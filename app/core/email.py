import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import os
from pathlib import Path
from ..core.config import settings
import aiosmtplib
import asyncio
from email.utils import formatdate
import datetime


class EmailClient:
    def __init__(self):
        self.sender_email = settings.EMAIL_USERNAME
        self.password = settings.EMAIL_PASSWORD
        self.smtp_server = settings.EMAIL_HOST
        self.smtp_port = settings.EMAIL_PORT
        self.templates_dir = os.path.join(Path(__file__).parent.parent, "templates", "email")
        self.template_env = Environment(loader=FileSystemLoader(self.templates_dir))
        
    def render_template(self, template_name, **context):
        """Render an HTML template with the given context"""
        try:
            # Add now function to context if not provided
            if 'now' not in context:
                context['now'] = lambda fmt: datetime.datetime.now().strftime(fmt)
            
            template = self.template_env.get_template(f"{template_name}.html")
            return template.render(**context)
        except Exception as e:
            print(f"Template rendering error: {str(e)}")
            # Fallback to a simple template
            if template_name == "verification_code":
                return f"""
                <html>
                <body>
                    <h1>Verification Code</h1>
                    <p>Hello,</p>
                    <p>Your verification code is: <strong>{context.get('code', 'N/A')}</strong></p>
                    <p>This code will expire in 30 minutes.</p>
                </body>
                </html>
                """
            else:
                return f"""
                <html>
                <body>
                    <h1>Welcome!</h1>
                    <p>Hello {context.get('user_name', '')},</p>
                    <p>Thank you for joining our platform.</p>
                    {f'<p>Your code is: <strong>{context.get("otp", "")}</strong></p>' if context.get('otp') else ''}
                </body>
                </html>
                """
        
    async def send_email_async(self, to_email, subject, template_name, **context):
        """Send an email asynchronously"""
        try:
            # Existing code for template rendering...
            html_content = self.render_template(template_name, **context)


            # Create the email message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = to_email
            message["Date"] = formatdate(localtime=True)

            # Attach HTML content
            part = MIMEText(html_content, "html")
            message.attach(part)

            print(f"Connecting to SMTP server: {self.smtp_server}:{self.smtp_port}")
            print(f"Using TLS: True")

            # Modified SMTP connection parameters:
            await aiosmtplib.send(
            message,
            hostname=self.smtp_server,
            port=self.smtp_port,
            username=self.sender_email,
            password=self.password,
            start_tls=True,  # Use start_tls (STARTTLS) for port 587
            validate_certs=True,
            timeout=30
            )

            print(f"Email sent successfully to {to_email}")
            return True
        
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    def send_email_sync(self, to_email, subject, template_name, **context):
        """Send an email synchronously"""
        try:
            # Create the HTML content from template
            html_content = self.render_template(template_name, **context)
            
            # Create the email message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = to_email
            
            # Attach HTML content
            part = MIMEText(html_content, "html")
            message.attach(part)
            
            # Connect to SMTP server
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, to_email, message.as_string())
                
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False

# Helper functions for common emails
email_client = EmailClient()

async def send_verification_email(to_email, code, user_id=None):
    """Send verification code email"""
    try:
        # Try async first
        result = await email_client.send_email_async(
            to_email=to_email,
            subject="Your Lanceraa Verification Code",
            template_name="verification_code",
            code=code,
            user_id=user_id,
            app_name="Lanceraa",
            support_email=settings.SUPPORT_EMAIL
        )
        
        # If async fails, try sync as fallback
        if not result:
            print("Async email failed, trying synchronous method...")
            result = email_client.send_email_sync(
                to_email=to_email,
                subject="Your Lanceraa Verification Code",
                template_name="verification_code",
                code=code,
                user_id=user_id,
                app_name="Lanceraa",
                support_email=settings.SUPPORT_EMAIL
            )
            
        return result
    except Exception as e:
        print(f"Error in send_verification_email: {str(e)}")
        return False

async def send_welcome_email(to_email, user_name, otp=None):
    """Send welcome email after verification"""
    try:
        # Try async first
        result = await email_client.send_email_async(
            to_email=to_email,
            subject="Welcome to Lanceraa!",
            template_name="welcome",
            user_name=user_name,
            app_name=settings.APP_NAME,
            support_email=settings.SUPPORT_EMAIL,
            otp=otp  # Pass the OTP to the template
        )
        
        # If async fails, try sync as fallback
        if not result:
            print("Async email failed, trying synchronous method...")
            result = email_client.send_email_sync(
                to_email=to_email,
                subject="Welcome to Lanceraa!",
                template_name="welcome",
                user_name=user_name,
                app_name=settings.APP_NAME,
                support_email=settings.SUPPORT_EMAIL,
                otp=otp
            )
            
        return result
    except Exception as e:
        print(f"Error in send_welcome_email: {str(e)}")
        return False

async def send_password_reset_email(to_email, reset_code):
    """Send password reset email"""
    try:
        # Try async first
        result = await email_client.send_email_async(
            to_email=to_email,
            subject="Reset Your Lanceraa Password",
            template_name="password_reset",
            reset_code=reset_code,
            app_name="Lanceraa",
            support_email=settings.SUPPORT_EMAIL
        )
        
        # If async fails, try sync as fallback
        if not result:
            print("Async email failed, trying synchronous method...")
            result = email_client.send_email_sync(
                to_email=to_email,
                subject="Reset Your Lanceraa Password",
                template_name="password_reset",
                reset_code=reset_code,
                app_name="Lanceraa",
                support_email=settings.SUPPORT_EMAIL
            )
            
        return result
    except Exception as e:
        print(f"Error in send_password_reset_email: {str(e)}")
        return False