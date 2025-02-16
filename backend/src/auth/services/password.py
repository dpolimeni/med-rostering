from passlib.context import CryptContext


class PasswordHasher:
    def __init__(self, rounds: int = 12):
        """Initialize the password hasher with bcrypt.

        Args:
            rounds: Number of rounds for bcrypt (default=12)
        """
        # Configure the password context with bcrypt
        self.pwd_context = CryptContext(
            schemes=["bcrypt"], default="bcrypt", bcrypt__default_rounds=rounds
        )

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt.

        Args:
            password: The plain-text password to hash

        Returns:
            str: The hashed password
        """
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash.

        Args:
            plain_password: The plain-text password to verify
            hashed_password: The hashed password to check against

        Returns:
            bool: True if the password matches, False otherwise
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def need_rehash(self, hashed_password: str) -> bool:
        """Check if a password needs to be rehashed.

        Useful when you want to upgrade security parameters.

        Args:
            hashed_password: The hashed password to check

        Returns:
            bool: True if the password should be rehashed
        """
        return self.pwd_context.needs_update(hashed_password)
