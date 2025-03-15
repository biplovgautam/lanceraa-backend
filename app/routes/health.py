from fastapi import APIRouter
from ..core.config import settings
from ..core.email import send_verification_email

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)

@router.get("")
async def health_check():
    """
    Health check endpoint to verify that the API is running
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "app_name": settings.APP_NAME
    }
@router.post("/test-email")
async def test_email(email: str):
    """Test endpoint to verify email functionality"""
    try:
        print(f"Testing email system to: {email}")
        
        # Print email configuration
        print(f"Email configuration:")
        print(f"  HOST: {settings.EMAIL_HOST}")
        print(f"  PORT: {settings.EMAIL_PORT}")
        print(f"  USERNAME: {settings.EMAIL_USERNAME[:3]}...{settings.EMAIL_USERNAME[-8:] if len(settings.EMAIL_USERNAME) > 10 else ''}")
        print(f"  PASSWORD SET: {'Yes' if settings.EMAIL_PASSWORD else 'No'}")
        
        # Test verification email
        verification_code = '123456'
        user_id = 'test-user-id'
        
        # Check for template directory
        import os
        from pathlib import Path
        
        template_dir = os.path.join(Path(__file__).parent.parent, "templates", "email")
        
        print(f"Template directory: {template_dir}")
        print(f"Directory exists: {os.path.exists(template_dir)}")
        
        if os.path.exists(template_dir):
            print(f"Files in directory: {os.listdir(template_dir)}")
        
        # Try alternate approach with standard smtplib (as a test)
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            print("Attempting direct SMTP connection as fallback...")
            
            msg = MIMEMultipart()
            msg['From'] = settings.EMAIL_USERNAME
            msg['To'] = email
            msg['Subject'] = 'Test Email from Lanceraa API'
            
            body = f'This is a test email to verify SMTP connection. Your code is: {verification_code}'
            msg.attach(MIMEText(body, 'plain'))
            
            try:
                server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                server.ehlo()
                server.starttls()  # Use STARTTLS for security
                server.ehlo()
                server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
                text = msg.as_string()
                server.sendmail(settings.EMAIL_USERNAME, email, text)
                server.close()
                print("Direct SMTP test: SUCCESS")
                direct_smtp_success = True
            except Exception as smtp_error:
                print(f"Direct SMTP test: FAILED - {str(smtp_error)}")
                direct_smtp_success = False
        except Exception as alt_error:
            print(f"Error in alternate approach: {str(alt_error)}")
            direct_smtp_success = False
        
        # Try original method
        result = await send_verification_email(email, verification_code, user_id)
        
        return {
            "success": result,
            "direct_smtp_test": direct_smtp_success if 'direct_smtp_success' in locals() else None,
            "message": "Email test completed - check server logs for details",
            "email_config": {
                "host": settings.EMAIL_HOST,
                "port": settings.EMAIL_PORT,
                "username_set": bool(settings.EMAIL_USERNAME),
                "password_set": bool(settings.EMAIL_PASSWORD),
                "template_dir_exists": os.path.exists(template_dir)
            }
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "success": False, 
            "error": str(e)
        }