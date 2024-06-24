from flask_bcrypt import Bcrypt

from .user_service import (
    get_user_by_id, get_user_by_email, login, verify_email, verify_email_resend,
    save_user, set_user_individual_data, add_project_log, update_user, delete_user
)
from .project_service import (
    get_project_by_id, get_project_list, get_comment_list, get_comment,
    save_project, add_comment, update_project, update_comment, delete_project, delete_comment
)
from .routine import decimal_to_float
from .auth import hash_password, verify_password, create_token, decode_token, token_required

bcrypt = Bcrypt()
