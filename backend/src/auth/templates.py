RESET_PASSWORD = """
<html>
    <body>
        <h2>Password Reset Request</h2>
        <p>Click the link below to reset your password. This link will expire in {expire} minutes.</p>
        <p><a href="{reset_link}">Reset Password</a></p>
        <p>If you didn't request this, please ignore this email.</p>
    </body>
</html>
"""

CONFIRM_REGISTRATION = """
<html>
    <body>
        <h2>Confirm Registration</h2>
        <p>Click the link below to confirm your registration. This link will expire in {expire} minutes.</p>
        <p><a href="{confirm_link}">Confirm Registration</a></p>
        <p>If you didn't request this, please ignore this email.</p>
    </body>
</html>

"""
