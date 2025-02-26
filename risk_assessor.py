def assess_s3_buckets(buckets: list) -> list:
    findings = []
    for bucket in buckets:
        bucket_name = bucket.get("bucket_name")
        # Check if the bucket is publicly accessible
        if bucket.get("public_access"):
            findings.append({
                "resource": bucket_name,
                "issue": "Bucket is public",
                "severity": "High"
            })
        # Check for encryption
        if not bucket.get("encryption"):
            findings.append({
                "resource": bucket_name,
                "issue": "Bucket not encrypted",
                "severity": "Medium"
            })
    return findings

def assess_iam_roles(roles: list) -> list:
    """
    Evaluate IAM role configurations for overly permissive policies.
    
    :param roles: List of IAM role configurations.
    :return: List of risk findings.
    """
    findings = []
    for role in roles:
        role_name = role.get("role_name")
        policies = role.get("policies", [])
        # Example check: flag if a role has 'FullAccess'
        if any("FullAccess" in policy for policy in policies):
            findings.append({
                "resource": role_name,
                "issue": "Role has FullAccess policies",
                "severity": "Critical"
            })
    return findings

def assess_ec2_instances(instances: list) -> list:
    """
    Evaluate EC2 instances for potential security issues.
    
    :param instances: List of EC2 instance configurations.
    :return: List of risk findings.
    """
    findings = []
    for instance in instances:
        instance_id = instance.get("instance_id")
        # Example: Check if an instance is publicly accessible
        if instance.get("public_ip"):
            findings.append({
                "resource": instance_id,
                "issue": "Instance has public IP",
                "severity": "Medium"
            })
    return findings

def aggregate_findings(data: dict) -> list:
    """
    Run all risk assessments and aggregate findings.
    
    :param data: Configuration data dictionary.
    :return: Combined list of all findings.
    """
    findings = []
    findings.extend(assess_s3_buckets(data.get("s3_buckets", [])))
    findings.extend(assess_iam_roles(data.get("iam_roles", [])))
    findings.extend(assess_ec2_instances(data.get("ec2_instances", [])))
    return findings

if __name__ == "__main__":
    # This block can be used for quick testing
    from data_fetcher import fetch_data
    bucket = 'enterprise-cspm'
    key = 'sample_data.json'
    sample_data = fetch_data(bucket, key)
    results = aggregate_findings(sample_data)
    print("Risk Findings:")
    for finding in results:
        print(finding)
