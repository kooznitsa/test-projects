# from . import link_schemas as ls
# from . import phone_codes
# from . import timezones
# from . import tags
# from . import statuses
# from . import messages
# from . import customers
# from . import mailouts

from api.schemas.link_schemas import CustomerTag, MailoutTag, MailoutCustomer, MailoutPhoneCode
from api.schemas.phone_codes import PhoneCodeInput, PhoneCodeOutput, PhoneCode
from api.schemas.timezones import TimezoneInput, TimezoneOutput, Timezone
from api.schemas.tags import TagInput, TagOutput, Tag
from api.schemas.statuses import StatusInput, StatusOutput, Status
from api.schemas.messages import MessageInput, MessageOutput, Message
from api.schemas.customers import CustomerInput, CustomerOutput, Customer
from api.schemas.mailouts import MailoutInput, MailoutOutput, Mailout

CustomerOutput.update_forward_refs()
