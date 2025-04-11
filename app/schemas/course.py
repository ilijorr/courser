from pydantic import BaseModel, Field
import uuid

from enums.course import CourseCategory

class CourseBase(BaseModel):
    id: uuid.UUID = Field(
            default_factory = uuid.uuid4,
            exclude=True,
            description="uuid generated with every request.")
    uni_id: int = Field(..., ge=1,
                        examples=[3])
    is_summer: bool = Field(...,
                            examples=[True, False])
    name: str = Field(..., min_length=1, max_length=256,
                      examples=["Algebra", "Object Oriented Programming"])
    category: CourseCategory = Field(...,
                                     examples=[CourseCategory.MATHEMATICS])

class CourseRelational(BaseModel):
    ects: int = Field(..., ge=1,
                      examples=[6])

class CourseVector(BaseModel):
    description: str = Field(..., min_length=20, max_length=1500,
                             examples=["This course provides a comprehensive introduction to fundamental algebraic concepts and techniques essential for advanced mathematics and real-world applications. Topics include linear and quadratic equations, inequalities, functions (polynomial, rational, exponential, logarithmic), systems of equations, and matrices. Students will explore graphing techniques, transformations, and algebraic modeling to solve practical problems. Emphasis is placed on developing analytical reasoning and problem-solving skills through theoretical and applied exercises. The course serves as a foundation for calculus, statistics, and other STEM disciplines, ensuring students gain the algebraic proficiency needed for academic and professional success. Prerequisites: Basic algebra skills are recommended."])

class CourseCreate(CourseBase, CourseRelational, CourseVector):
    pass
