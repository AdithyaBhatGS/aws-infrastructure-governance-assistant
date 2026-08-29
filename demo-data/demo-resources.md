# This markdown contains set of demo data just for testing the `api:/resource_discovery`

1. Create 2 s3 buckets:

   ```bash
   aws s3 mb s3://amzzn-aqkkqkk101
   aws s3 mb s3://amzzn-aqkkqkk105
   ```

   ```bash
    aws s3 rb s3://amzzn-aqkkqkk101
   ```

2. Create and delete the ebs volume:

   ```bash
   aws ec2 create-volume --volume-type gp2 --size 2 --availability-zone us-east-2b
   ```

   ```bash
   aws ec2 delete-volume \
   --volume-id <volume-id>
   ```

3. Create & destroy EIP:

   ```bash
   aws ec2 allocate-address
   ```

   ```bash
   aws ec2 release-address \
   --allocation-id <eip>
   ```

4. Create & destroy a nat gateway:

   ```bash
   aws ec2 create-nat-gateway \
   --subnet-id <subnet-id> \
   --allocation-id <allocation-id>
   ```

   ```bash
   aws ec2 delete-nat-gateway \
   --nat-gateway-id <nat-id>
   ```

5. Create a load balancer:

   ```bash
   aws elbv2 create-load-balancer \
   --name my-load-balancer \
   --subnets subnet-id2 subnet-id1
   ```

   ```
   aws elbv2 delete-load-balancer \
   --load-balancer-arn <lb-arn>
   ```
