"""
Complete Pydantic Learning Example
Based on AI_AGENT Pre-Marriage Counseling Knowledge Base
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ValidationError
import json


# ============================================================================
# LEVEL 1: SIMPLE MODELS (Basic Pydantic Usage)
# ============================================================================

class SimpleCandidate(BaseModel):
    """Simplest example - Just required fields"""
    name: str
    age: int
    profession: str


# Example 1.1: Creating and validating data
print("=" * 60)
print("LEVEL 1: Simple Models")
print("=" * 60)

# ✅ CORRECT: All required fields with correct types
candidate1 = SimpleCandidate(name="Amit", age=28, profession="Engineer")
print(f"✅ Valid: {candidate1}")

# ❌ ERROR: Missing required field
try:
    candidate2 = SimpleCandidate(name="Priya", age=25)
except ValidationError as e:
    print(f"❌ Error (missing field): {e.errors()[0]['msg']}")

# ❌ ERROR: Wrong type
try:
    candidate3 = SimpleCandidate(name="Raj", age="twenty-five", profession="Doctor")
except ValidationError as e:
    print(f"❌ Error (wrong type): {e.errors()[0]['msg']}")


# ============================================================================
# LEVEL 2: OPTIONAL FIELDS & DEFAULTS
# ============================================================================

class CandidateWithOptional(BaseModel):
    """Adding optional and default fields"""
    name: str
    age: int
    profession: str
    location: Optional[str] = None  # Optional field
    income_range: str = "Not Specified"  # Default value


print("\n" + "=" * 60)
print("LEVEL 2: Optional Fields & Defaults")
print("=" * 60)

# ✅ Required fields only (optional fields default to None)
candidate4 = CandidateWithOptional(name="Neha", age=26, profession="Lawyer")
print(f"✅ Minimal data: {candidate4}")

# ✅ With optional fields provided
candidate5 = CandidateWithOptional(
    name="Arjun", 
    age=30, 
    profession="Architect",
    location="Mumbai",
    income_range="50-75 LPA"
)
print(f"✅ Complete data: {candidate5}")


# ============================================================================
# LEVEL 3: LISTS AND DICTIONARIES
# ============================================================================

class CandidateWithLists(BaseModel):
    """Working with lists and dictionaries"""
    name: str
    qualifications: List[str]  # List of strings
    social_media: Dict[str, str]  # Dictionary of profiles
    skills: List[str] = Field(default_factory=list)  # Default empty list


print("\n" + "=" * 60)
print("LEVEL 3: Lists and Dictionaries")
print("=" * 60)

candidate6 = CandidateWithLists(
    name="Kavya",
    qualifications=["BTech CS", "MBA"],
    social_media={"linkedin": "kavya123", "instagram": "kavya_tech"},
    skills=["Python", "Machine Learning", "Project Management"]
)
print(f"✅ With lists & dicts: {candidate6}")
print(f"   Qualifications: {candidate6.qualifications}")
print(f"   LinkedIn: {candidate6.social_media['linkedin']}")


# ============================================================================
# LEVEL 4: NESTED MODELS (Complex Structures)
# ============================================================================

class FamilyMember(BaseModel):
    """Nested model: Family member info"""
    name: str
    relationship: str  # father, mother, sibling
    profession: Optional[str] = None
    age: Optional[int] = None


class FamilyBackground(BaseModel):
    """Model containing other models"""
    family_members: List[FamilyMember]  # List of FamilyMember objects
    cultural_values: List[str] = Field(default_factory=list)
    family_business: Optional[str] = None


class CompleteCandidate(BaseModel):
    """Full candidate with nested data"""
    name: str
    age: int
    family: FamilyBackground  # Nested model


print("\n" + "=" * 60)
print("LEVEL 4: Nested Models")
print("=" * 60)

candidate7 = CompleteCandidate(
    name="Rahul",
    age=28,
    family=FamilyBackground(
        family_members=[
            FamilyMember(name="Mr. Sharma", relationship="father", profession="Business"),
            FamilyMember(name="Mrs. Sharma", relationship="mother", age=55),
            FamilyMember(name="Priya", relationship="sister", age=25, profession="Teacher")
        ],
        cultural_values=["Respect", "Education", "Hard Work"],
        family_business="Import-Export"
    )
)
print(f"✅ Nested data: {candidate7.name}")
print(f"   Family members: {len(candidate7.family.family_members)}")
for member in candidate7.family.family_members:
    print(f"   - {member.name} ({member.relationship})")


# ============================================================================
# LEVEL 5: JSON SERIALIZATION & DESERIALIZATION
# ============================================================================

print("\n" + "=" * 60)
print("LEVEL 5: JSON Serialization/Deserialization")
print("=" * 60)

# Convert to dict
candidate_dict = candidate7.model_dump()
print(f"✅ To Dictionary:\n{json.dumps(candidate_dict, indent=2)}\n")

# Convert to JSON string
candidate_json = candidate7.model_dump_json(indent=2)
print(f"✅ To JSON String:\n{candidate_json}\n")

# Parse from JSON string
json_string = '''
{
    "name": "Divya",
    "age": 27,
    "family": {
        "family_members": [
            {"name": "Dr. Patel", "relationship": "father", "profession": "Doctor"}
        ],
        "cultural_values": ["Education", "Health"]
    }
}
'''
candidate8 = CompleteCandidate.model_validate_json(json_string)
print(f"✅ From JSON:\n{candidate8.name}, Age: {candidate8.age}")


# ============================================================================
# LEVEL 6: PRACTICAL EXAMPLE - REAL USE CASE
# ============================================================================

print("\n" + "=" * 60)
print("LEVEL 6: Real Use Case - Pre-Marriage Counseling")
print("=" * 60)

class PsychometricReport(BaseModel):
    personality_type: str
    compatibility_score: float
    report: Optional[str] = None


class Candidate(BaseModel):
    """Complete candidate for matching"""
    primary_info: dict  # name, age, profession
    interests: List[str]
    psychometric: PsychometricReport
    
    def get_profile_summary(self) -> str:
        return f"{self.primary_info['name']} - {self.primary_info['profession']} - {self.psychometric.personality_type}"


# Create candidates for matching
bride = Candidate(
    primary_info={"name": "Anjali", "age": 26, "profession": "Doctor"},
    interests=["Reading", "Cooking", "Yoga"],
    psychometric=PsychometricReport(
        personality_type="ISFJ",
        compatibility_score=8.2,
        report="Caring and organized individual"
    )
)

groom = Candidate(
    primary_info={"name": "Vikram", "age": 28, "profession": "Engineer"},
    interests=["Sports", "Technology", "Cooking"],
    psychometric=PsychometricReport(
        personality_type="ISTJ",
        compatibility_score=8.0,
        report="Dependable and practical individual"
    )
)

print(f"Bride Profile: {bride.get_profile_summary()}")
print(f"Groom Profile: {groom.get_profile_summary()}")
print(f"\nCommon Interests: {set(bride.interests) & set(groom.interests)}")
print(f"Compatibility: {(bride.psychometric.compatibility_score + groom.psychometric.compatibility_score) / 2:.1f}/10")


# ============================================================================
# LEVEL 7: VALIDATION EXAMPLES
# ============================================================================

print("\n" + "=" * 60)
print("LEVEL 7: Validation - What Pydantic Catches")
print("=" * 60)

test_cases = [
    ("Age as string (auto-converts)", {"name": "Test", "age": "25", "profession": "Engineer"}),
    ("Missing field", {"name": "Test", "profession": "Engineer"}),
    ("Invalid JSON structure", {"name": "Test", "age": 25}),
]

for description, data in test_cases:
    try:
        result = SimpleCandidate(**data)
        print(f"✅ {description}: Success")
    except ValidationError as e:
        print(f"❌ {description}: {e.errors()[0]['msg']}")
