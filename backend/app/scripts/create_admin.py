import re
from getpass import getpass

from pydantic import EmailStr, TypeAdapter, ValidationError
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError

from app.core.security import hash_password
from app.db.database import SessionLocal
from app.models.admin_user import AdminUser


email_validator = TypeAdapter(EmailStr)

USERNAME_PATTERN = re.compile(
    r"^[A-Za-z0-9_.-]{3,50}$"
)


def main() -> None:
    print("\nCreate Bajirao AI Portfolio Admin")
    print("---------------------------------\n")

    username = input(
        "Admin username: "
    ).strip().lower()

    if not USERNAME_PATTERN.fullmatch(username):
        print(
            "Invalid username. Use 3-50 letters, "
            "numbers, dots, underscores or hyphens."
        )
        return

    email_input = input(
        "Admin email: "
    ).strip().lower()

    try:
        email = str(
            email_validator.validate_python(
                email_input
            )
        )
    except ValidationError:
        print("Invalid email address.")
        return

    password = getpass(
        "Admin password: "
    )

    if len(password) < 12:
        print(
            "Password must contain at least "
            "12 characters."
        )
        return

    password_confirmation = getpass(
        "Confirm admin password: "
    )

    if password != password_confirmation:
        print("Passwords do not match.")
        return

    with SessionLocal() as database_session:
        existing_statement = select(
            AdminUser
        ).where(
            or_(
                AdminUser.username == username,
                AdminUser.email == email,
            )
        )

        existing_admin = database_session.scalar(
            existing_statement
        )

        if existing_admin is not None:
            print(
                "An admin with this username "
                "or email already exists."
            )
            return

        admin = AdminUser(
            username=username,
            email=email,
            password_hash=hash_password(password),
            is_active=True,
            is_superuser=True,
        )

        database_session.add(admin)

        try:
            database_session.commit()
            database_session.refresh(admin)

        except IntegrityError:
            database_session.rollback()

            print(
                "Admin creation failed because "
                "the username or email already exists."
            )
            return

        print("\nAdmin account created successfully.")
        print(f"Admin ID: {admin.id}")
        print(f"Username: {admin.username}")
        print(f"Email: {admin.email}")


if __name__ == "__main__":
    main()