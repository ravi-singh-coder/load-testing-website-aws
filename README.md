# Loctus

To host a website on AWS, set up an AWS account and launch an EC2 instance. Install a web server like Apache or Nginx on your instance. Upload your website files to the server, and configure security groups to allow HTTP access. Optionally, use Route 53 to manage your domain name.
Locust is an open-source load testing tool that allows you to define user behavior in Python code. It simulates concurrent users to test the performance and scalability of your applications. Locust provides real-time metrics and customizable test scenarios for effective load testing.

## Prerequisites

- AWS Account
- SSH Key Pair
- Domain Name (optional)

## Deployment Steps

1. **Set Up AWS Account**
   - Sign up for an AWS account.
   - Log in to the AWS Management Console.

2. **Launch an EC2 Instance**
   - Navigate to the EC2 Dashboard.
   - Launch a new EC2 instance with Amazon Linux 2 AMI.
   - Configure the instance (t2.micro, security group with HTTP and SSH access).
   - Launch the instance and download the key pair.

3. **Configure the EC2 Instance**
   - Connect to the instance via SSH:
     ```bash
     ssh -i your-key-pair.pem ec2-user@your-instance-public-dns
     ```
   - Install a web server (Apache or Nginx):
     - Apache:
       ```bash
       sudo yum update -y
       sudo yum install httpd -y
       sudo systemctl start httpd
       sudo systemctl enable httpd
       ```
     - Nginx:
       ```bash
       sudo amazon-linux-extras install nginx1.12 -y
       sudo systemctl start nginx
       sudo systemctl enable nginx
       ```

4. **Deploy Website**
   - Upload your website files to the server:
     ```bash
     scp -i your-key-pair.pem -r /path/to/your/website/files ec2-user@your-instance-public-dns:/var/www/html/
     ```
   - Verify the deployment by navigating to your instance's public DNS in a web browser.

5. **Update DNS Settings (Optional)**
   - Purchase a domain name.
   - Use AWS Route 53 to route traffic to your instance.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
