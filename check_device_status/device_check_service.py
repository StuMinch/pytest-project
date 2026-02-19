#!/usr/bin/env python3
"""
Device Availability Checker Service for Sauce Labs

This service continuously polls Sauce Labs private device availability
and executes pytest scripts when devices become available.
"""

import os
import sys
import time
import requests
import json
import subprocess
from typing import List, Optional
from datetime import datetime


class SauceLabsDeviceChecker:
    """Manages polling and testing for Sauce Labs private devices."""
    
    def __init__(
        self,
        device_ids: List[str],
        api_url: str = "https://api.us-west-1.saucelabs.com/v1/rdc/device-management/devices",
        poll_interval: int = 10,
        max_runs: Optional[int] = None
    ):
        """
        Initialize the device checker.
        
        Args:
            device_ids: List of device IDs to monitor
            api_url: Sauce Labs device management API URL
            poll_interval: Seconds between status checks
            max_runs: Maximum number of test runs (None for infinite)
        """
        self.device_ids = device_ids
        self.api_url = api_url
        self.poll_interval = poll_interval
        self.max_runs = max_runs
        self.selected_device_id = None
        
        # Get credentials from environment variables
        self.username = os.environ.get("SAUCE_USERNAME")
        self.access_key = os.environ.get("SAUCE_ACCESS_KEY")
        
        if not self.username or not self.access_key:
            raise ValueError(
                "SAUCE_USERNAME and SAUCE_ACCESS_KEY environment variables must be set"
            )
    
    def _log(self, message: str) -> None:
        """Log a message with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def _get_device_status(self, device_id: str) -> Optional[str]:
        """
        Fetch the status of a specific device from Sauce Labs API.
        
        Args:
            device_id: The device ID to check
            
        Returns:
            Device status string or None if not found
        """
        try:
            response = requests.get(
                self.api_url,
                auth=(self.username, self.access_key),
                timeout=10
            )
            response.raise_for_status()
            
            devices = response.json()
            for device in devices:
                if device.get("id") == device_id:
                    return device.get("state")
            
            return None
        except requests.exceptions.RequestException as e:
            self._log(f"Error fetching device status: {e}")
            return None
    
    def wait_for_devices(self) -> str:
        """
        Poll device availability until one becomes available.
        
        Returns:
            The ID of the available device
        """
        while True:
            for device_id in self.device_ids:
                status = self._get_device_status(device_id)
                self._log(f"[{device_id}] Status: {status or 'NOT FOUND'}")
                
                if status == "AVAILABLE":
                    self._log(f"Device {device_id} is AVAILABLE — proceeding with test run.")
                    self.selected_device_id = device_id
                    return device_id
            
            self._log(f"Waiting {self.poll_interval} seconds before checking again...")
            time.sleep(self.poll_interval)
    
    def run_test_suite(self, test_script: str) -> bool:
        """
        Execute a pytest test script using the configured selected device.

        Args:
            test_script: Path to the pytest script to execute

        Returns:
            True if successful, False otherwise
        """
        try:
            env = os.environ.copy()
            if self.selected_device_id:
                env["SELECTED_DEVICE_ID"] = self.selected_device_id

            self._log(f"Executing pytest script: {test_script}")
            # Run pytest quietly for the single script
            result = subprocess.run([
                sys.executable, "-m", "pytest", "-q", test_script
            ], env=env, check=False)

            if result.returncode == 0:
                self._log(f"Pytest {test_script} completed successfully")
                return True
            else:
                self._log(f"Pytest {test_script} failed with exit code {result.returncode}")
                return False
        except FileNotFoundError:
            self._log("Error: pytest not found in the current Python environment.")
            return False
        except Exception as e:
            self._log(f"Error executing pytest: {e}")
            return False
    
    def start_service(self, test_scripts: Optional[List[str]] = None) -> None:
        """
        Start the device monitoring service and execute pytest when devices are available.

        Args:
            test_scripts: List of pytest script paths to run when a device becomes available
        """
        self._log("=" * 50)
        self._log("Device Availability Checker Service Started")
        self._log("=" * 50)
        self._log(f"Monitoring devices: {', '.join(self.device_ids)}")
        self._log(f"Poll interval: {self.poll_interval} seconds")
        if self.max_runs:
            self._log(f"Max runs: {self.max_runs}")
        else:
            self._log("Running indefinitely (Ctrl+C to stop)")
        self._log("=" * 50)
        self._log("")
        
        run_count = 0
        
        try:
            while True:
                run_count += 1
                
                if self.max_runs and run_count > self.max_runs:
                    self._log(f"Reached maximum runs ({self.max_runs}). Stopping service.")
                    break
                
                self._log("=" * 50)
                self._log(f"Run number {run_count}")
                self._log("=" * 50)
                
                # Normalize input to a list (done once per run loop)
                if test_scripts is None:
                    scripts = ["test_features.py"]
                elif isinstance(test_scripts, str):
                    scripts = [test_scripts]
                else:
                    scripts = list(test_scripts)

                # For each script, check device availability and then run the test.
                # This ensures we re-check devices between tests.
                for script in scripts:
                    self.wait_for_devices()
                    self.run_test_suite(script)
                
                self._log("")
        
        except KeyboardInterrupt:
            self._log("")
            self._log("=" * 50)
            self._log("Service stopped by user (Ctrl+C)")
            self._log("=" * 50)
            sys.exit(0)
        except Exception as e:
            self._log(f"Unexpected error in service: {e}")
            sys.exit(1)


def main():
    """Main entry point for the service."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Sauce Labs Device Availability Checker Service"
    )
    parser.add_argument(
        "--devices",
        nargs="+",
        default=["iPhone_SE_2020_POC132", "iPhone_SE_2020_POC124"],
        help="Device IDs to monitor (space-separated)"
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=10,
        help="Seconds between status checks (default: 10)"
    )
    parser.add_argument(
        "--max-runs",
        type=int,
        default=None,
        help="Maximum number of test runs (default: infinite)"
    )
    parser.add_argument(
        "--api-url",
        default="https://api.us-west-1.saucelabs.com/v1/rdc/device-management/devices",
        help="Sauce Labs device management API URL"
    )
    # Use --test-script to specify pytest script
    parser.add_argument(
        "--test-script",
        nargs='+',
        default=["test_features.py"],
        help="One or more pytest scripts to execute when a device becomes available"
    )
    
    args = parser.parse_args()
    
    try:
        checker = SauceLabsDeviceChecker(
            device_ids=args.devices,
            api_url=args.api_url,
            poll_interval=args.poll_interval,
            max_runs=args.max_runs
        )
        checker.start_service(test_scripts=args.test_script)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
