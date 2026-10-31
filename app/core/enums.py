import enum
class CategoryEnum(str, enum.Enum):
    FAMILY = "Family"
    FRIENDS = "Friends"
    WORK = "Work"
    OTHER = "Other"