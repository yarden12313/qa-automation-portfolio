def compare_environments(env1, env2) -> dict:
    comps1 = {comp["name"]: comp for comp in env1["components"]}
    comps2 = {comp["name"]: comp for comp in env2["components"]}

    # component names that exist in env1 but not in env2
    missing_in_env2 = [key for key in comps1.keys() if key not in comps2]

    # component names that exist in env2 but not in env1
    missing_in_env1 = [key for key in comps2.keys() if key not in comps1]

    # list of dicts for components that exist in BOTH but have different versions
    version_mismatches = []
    for key, value in comps1.items():
        if key in comps2 and comps2[key]["version"] != comps1[key]["version"]:
            version_mismatches.append({"name": key, "env1_version": comps1[key]["version"], "env2_version": comps2[key]["version"]})

    # list of component names that exist in both but have different "enabled" status
    enabled_mismatches = [key for key in comps1.keys() if key in comps2 and comps2[key]["enabled"] != comps1[key]["enabled"]]

    return {"missing_in_env2": missing_in_env2,
            "missing_in_env1": missing_in_env1,
            "version_mismatches": version_mismatches,
            "enabled_mismatches": enabled_mismatches}

def test_compare_environments():
    testing_env = {
        "version": "4.2.1",
        "components": [
            {"name": "scanner-engine", "version": "2.1.0", "enabled": True},
            {"name": "results-processor", "version": "1.8.3", "enabled": True},
            {"name": "report-generator", "version": "3.0.1", "enabled": False},
            {"name": "data-connector", "version": "1.2.0", "enabled": True},
        ]
    }

    rc_env = {
        "version": "4.2.1",
        "components": [
            {"name": "scanner-engine", "version": "2.1.0", "enabled": True},
            {"name": "results-processor", "version": "1.9.0", "enabled": True},
            {"name": "report-generator", "version": "3.0.1", "enabled": True},
            {"name": "data-connector-v2", "version": "2.0.0", "enabled": True},
        ]
    }
    compared_environments = compare_environments(testing_env, rc_env)
    expected_result = {"missing_in_env2": ["data-connector"],
            "missing_in_env1": ["data-connector-v2"],
            "version_mismatches": [
        {
            "name": "results-processor",
            "env1_version": "1.8.3",
            "env2_version": "1.9.0"
        }
    ],
            "enabled_mismatches": ["report-generator"]}
    assert compared_environments == expected_result, "Environments do not have expected differences."