from app.models.history import DriftHistoryEntry
import json

class HistoryService:
    """Service for comparing drift snapshots across time and summarizing changes."""

    def _filter_environment(self, snapshots: list[dict], environment: str) -> list[dict]:
        """Filter snapshots for a specific deployment environment.

        Args:
            snapshots (list[dict]): Snapshot records to evaluate.
            environment (str): Deployment environment to match.

        Returns:
            list[dict]: Snapshot records belonging to the requested environment.
        """
        return [
            snapshot
            for snapshot in snapshots
            if snapshot.get("Environment", []) == environment
        ]

    def _extract_drift_state(self, snapshot: dict) -> list[dict]:
        """Extract drift details for all resources in a snapshot.

        Args:
            snapshot (dict): Snapshot payload containing stack drift results.

        Returns:
            list[dict]: Resource-level drift records with a normalized structure.
        """
        drift_state = []

        for stack in snapshot.get("Results", []):
            for resource in stack.get("resources", []):
                differences = resource.get("property_differences", [])

                if not differences:
                    continue

                drift_state.append({
                    "stack_name": stack.get("stack_name"),
                    "logical_id": resource.get("logical_id"),
                    "resource_type": resource.get("resource_type"),
                    "property_differences": resource.get("property_differences")
                })

        return drift_state

    def _normalize_property_differences(self, property_differences: list[dict]) -> list[dict]:
        """Sort property differences for stable comparisons.

        Args:
            property_differences (list[dict]): Property difference records.

        Returns:
            list[dict]: Property differences sorted by path, expected value,
                difference type, and actual value.
        """
        return sorted(
            property_differences,
            key=lambda difference: (
                difference.get("PropertyPath", ""),
                difference.get("ExpectedValue", ""),
                difference.get("DifferenceType", ""),
                difference.get("ActualValue", "")
            )
        )

    def _normalize_drift_state(self, drift_state: list[dict]) -> list[dict]:
        """Normalize a drift state for deterministic comparison.

        Args:
            drift_state (list[dict]): Resource-level drift records.

        Returns:
            list[dict]: Normalized resource drift records sorted consistently.
        """
        normalized_state = []

        for resource in drift_state:
            normalized_property_differences = (
                self._normalize_property_differences(
                    resource.get("property_differences", [])
                )
            )
            normalized_resource = {
                "stack_name": resource.get("stack_name", ""),
                "logical_id": resource.get("logical_id", ""),
                "resource_type": resource.get("resource_type", ""),
                "property_differences": normalized_property_differences
            }

            normalized_state.append(normalized_resource)

        return sorted(
            normalized_state,
            key=lambda item: (
                item.get("stack_name", ""),
                item.get("logical_id", ""),
                item.get("resource_type", "")
            )
        )

    def _resource_key(self, resource: dict) -> tuple:
        """Build a stable key for a resource record.

        Args:
            resource (dict): Resource drift metadata.

        Returns:
            tuple: A tuple of stack name, logical ID, and resource type.
        """
        return (
            resource.get("stack_name"),
            resource.get("logical_id"),
            resource.get("resource_type")
        )

    def _compare_property_differences(self, previous_differences: list[dict], current_differences: list[dict]) -> dict:
        """Compare property differences between two drift states.

        Args:
            previous_differences (list[dict]): Property differences from the older scan.
            current_differences (list[dict]): Property differences from the newer scan.

        Returns:
            dict: A dictionary containing added and removed property differences.
        """
        previous_map = {
            (
                difference.get("PropertyPath", ""),
                difference.get("ExpectedValue", ""),
                difference.get("DifferenceType", ""),
                difference.get("ActualValue", "")
            ): difference
            for difference in previous_differences
        }

        current_map = {
            (
                current.get("PropertyPath", ""),
                current.get("ExpectedValue", ""),
                current.get("DifferenceType", ""),
                current.get("ActualValue", "")
            ): current
            for current in current_differences
        }

        added = []
        removed = []

        for key, difference in current_map.items():
            if key not in previous_map:
                added.append(difference)

        for key, difference in previous_map.items():
            if key not in current_map:
                removed.append(difference)

        return {
            "added": added,
            "removed": removed
        }

    def _compare_drift_states(self, previous_state: list[dict], current_state: list[dict]) -> dict:
        """Compare previous and current drift states for resource changes.

        Args:
            previous_state (list[dict]): Drift state from the previous snapshot.
            current_state (list[dict]): Drift state from the current snapshot.

        Returns:
            dict: A dictionary containing added, removed, and changed resources.
        """
        previous_resources = {
            self._resource_key(resource): resource
            for resource in previous_state
        }

        current_resources = {
            self._resource_key(resource): resource
            for resource in current_state
        }

        added = []
        removed = []
        changed = []

        for key, resource in current_resources.items():
            if key not in previous_resources:
                added.append(resource)

        for key, resource in previous_resources.items():
            if key not in current_resources:
                removed.append(resource)

        for key in previous_resources.keys() & current_resources.keys():
            previous_resource = previous_resources.get(key)
            current_resource = current_resources.get(key)

            previous_differences = previous_resource.get(
                "property_differences",
                []
            )

            current_differences = current_resource.get(
                "property_differences",
                []
            )

            property_changes = self._compare_property_differences(
                previous_differences,
                current_differences
            )

            if property_changes.get("added") or property_changes.get("removed"):
                changed.append({
                    "stack_name": current_resource.get("stack_name"),
                    "logical_id": current_resource.get("logical_id"),
                    "resource_type": current_resource.get("resource_type"),
                    "property_changes": property_changes
                })

        return {
            "added": added,
            "removed": removed,
            "changed": changed
        }

    def _get_drift_changes(self, history: list[dict]) -> list[dict]:
        """Compute drift changes between consecutive historical snapshots.

        Args:
            history (list[dict]): Historical snapshots with their drift states.

        Returns:
            list[dict]: Drift change summaries for each snapshot transition.
        """
        changes = []

        normalized_history = []

        for snapshot in history:
            normalized_history.append({
                "scan_time": snapshot.get("scan_time"),
                "drift_state": self._normalize_drift_state(
                    snapshot.get("drift_state")
                )
            })

        for index in range(1, len(normalized_history)):
            previous_state = normalized_history[index - 1]
            current_state = normalized_history[index]

            delta = self._compare_drift_states(
                previous_state.get("drift_state"),
                current_state.get("drift_state")
            )

            total_drifts = len(
                current_state.get("drift_state", [])
            )

            if delta.get("added") or delta.get("removed") or delta.get("changed"):
                changes.append({
                    "scan_time": current_state.get("scan_time"),
                    "added": delta.get("added"),
                    "removed": delta.get("removed"),
                    "changed": delta.get("changed"),
                    "total_drifts": total_drifts
                })

        return changes

    def _build_history(self, snapshots: list[dict], environment: str) -> list[dict]:
        """Build a normalized history from snapshots for a specific environment.

        Args:
            snapshots (list[dict]): Raw snapshot records from DynamoDB.
            environment (str): Environment to include in the history.

        Returns:
            list[dict]: A normalized history of drift states and timestamps.
        """
        snapshots = self._filter_environment(
            snapshots,
            environment
        )

        return [
            {
                "scan_time": snapshot.get("ScanTime"),
                "drift_state": self._extract_drift_state(snapshot)
            }
            for snapshot in snapshots
        ]

    def get_history(self, snapshots: list[dict], environment: str) -> list[dict]:
        """Return the historical drift changes for an environment.

        Args:
            snapshots (list[dict]): Raw snapshot records to analyze.
            environment (str): Environment to evaluate.

        Returns:
            list[dict]: Drift changes observed across historical snapshots.
        """

        history = self._build_history(
            snapshots,
            environment
        )
        return self._get_drift_changes(history)

