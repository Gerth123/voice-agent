from enum import StrEnum


class AppointmentStatus(StrEnum):
    PROPOSED = "proposed"
    BOOKED = "booked"
    CANCELLED = "cancelled"


class AppointmentRequestStatus(StrEnum):
    DETECTED = "detected"
    NEEDS_CLARIFICATION = "needs_clarification"
    SLOT_FOUND = "slot_found"
    BOOKED = "booked"
    REJECTED = "rejected"


class AuditActorType(StrEnum):
    USER = "user"
    SYSTEM = "system"
    PROVIDER = "provider"
    N8N = "n8n"


class BookingMode(StrEnum):
    DISABLED = "disabled"
    SUGGEST_ONLY = "suggest_only"
    AUTO_BOOK_CLEAR_SLOTS = "auto_book_clear_slots"


class CalendarMode(StrEnum):
    READ_ONLY = "read_only"
    READ_WRITE = "read_write"


class CalendarProvider(StrEnum):
    ICAL = "ical"
    GOOGLE = "google"
    MICROSOFT = "microsoft"


class CallDirection(StrEnum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class CallStatus(StrEnum):
    RECEIVED = "received"
    COMPLETED = "completed"
    FAILED = "failed"
    MISSED = "missed"


class ConsentEvidenceType(StrEnum):
    SYSTEM_EVENT = "system_event"
    SPOKEN_CONFIRMATION = "spoken_confirmation"
    MANUAL = "manual"


class ConsentStatus(StrEnum):
    GIVEN = "given"
    DECLINED = "declined"
    NOT_REQUIRED = "not_required"
    UNKNOWN = "unknown"


class ConsentType(StrEnum):
    AI_DISCLOSURE = "ai_disclosure"
    AUDIO_RECORDING = "audio_recording"
    TRANSCRIPT_STORAGE = "transcript_storage"
    APPOINTMENT_BOOKING = "appointment_booking"


class ContactSource(StrEnum):
    CALL = "call"
    MANUAL = "manual"
    IMPORT = "import"


class DataSubjectType(StrEnum):
    OWNER_CONTACT = "owner_contact"
    THIRD_PARTY_CONTACT = "third_party_contact"


class DeleteMode(StrEnum):
    HARD_DELETE = "hard_delete"
    ANONYMIZE = "anonymize"


class NotificationChannel(StrEnum):
    WHATSAPP = "whatsapp"
    EMAIL = "email"
    TELEGRAM = "telegram"
    SLACK = "slack"


class NotificationStatus(StrEnum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


class ProviderDpaStatus(StrEnum):
    UNKNOWN = "unknown"
    REQUESTED = "requested"
    SIGNED = "signed"
    NOT_APPLICABLE = "not_applicable"


class UserRole(StrEnum):
    OWNER = "owner"
    ADMIN = "admin"
    USER = "user"

