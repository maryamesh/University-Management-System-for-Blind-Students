# University Management System for Blind Students

## Abstract

The University Management System for Blind Students is a specialized web-based platform designed to enhance the educational experience and administrative management for visually impaired students within a university setting. The primary purpose of this system is to provide an accessible, intuitive, and comprehensive management solution that caters specifically to the needs of blind students, enabling them to access course materials easily.

- **Scope:** The system encompasses key functionalities, including user authentication, course enrollment, lecture access, grade management, and real-time announcements. It integrates accessible technology to ensure that all user interfaces are compatible with screen readers and other assistive technologies, promoting an inclusive educational environment. The backend is built on TypeScript with a Supabase database, ensuring robust data handling and security. The frontend employs HTML, CSS, and JavaScript, enhanced with accessibility features to support navigation and interaction without visual cues.

- **Outcomes:** Upon deployment, the system achieved its objective of making educational management more accessible for visually impaired students. It significantly improved students' ability to independently manage their academic affairs, participate in courses, and access necessary academic resources with ease. Furthermore, the platform streamlined administrative processes by providing efficient tools to manage courses.

## Introduction

In the evolving landscape of educational technology, inclusivity and accessibility are paramount, particularly for students with visual impairments. This University Management System leverages cutting-edge technology to create an accessible, voice-activated platform that fosters an inclusive educational environment.

The system integrates Python scripts for PDF summarization and utilizes a BERT transformer architecture to summarize textual content, such as lecture notes and readings, providing concise, manageable information tailored to the needs of blind students.

## System Overview

Our University Management System is designed to provide a seamless and accessible educational management experience for visually impaired students. The system includes various user-friendly interfaces and backend functionalities to ensure comprehensive academic and administrative management.

### Architecture

The system architecture is built around a modular design, integrating various technologies to ensure robust performance and scalability. It employs a client-server model where the frontend interfaces with users and the backend handles data management.

### Technologies Used

- **Database:** Supabase
- **Backend:** TypeScript
- **Frontend:** HTML, CSS, JavaScript
- **Python Integration:** PDF Summarization and Text-to-Speech Conversion

## Literature Review

Existing Systems and Limitations:

| System Name | Description | Limitations |
| ----------- | ----------- | ----------- |
| UMS for Visually Impaired Students | A university management system designed for visually impaired users, focusing on voice commands. | Limited support for mobile devices |
| AccessUni | General university management platform with accessibility features such as high contrast and screen reader compatibility. | Does not include voice commands; primarily designed for low vision users, not fully blind. |
| EduAdapt | An educational portal with adaptive technologies including Braille support and audiobooks. | No integration of real-time communication or course management specific to university needs. |

## Technology Stack

### Frontend

- **HTML Structure:** A user-friendly and responsive dashboard for students.
- **CSS Design:** Enhances the user interface with visual feedback and smooth transitions.
- **JavaScript:** Manages dynamic content and interactivity, ensuring a seamless user experience.

### Backend: TypeScript with `rout.ts` Endpoints

- **Modular Routing:** Ensures clean and maintainable code.
- **Endpoint Definition:** Handles various HTTP requests related to system operations.
- **RESTful API Practices:** Manages resources using standard HTTP methods.

### Database: Supabase

Supabase serves as the core database platform, enabling scalability, real-time data updates, and robust user authentication.

### Python Integration

Python scripts are used for PDF summarization, enhancing accessibility for blind students by providing concise document summaries.

## System Design

### Database Tables

- **Courses, Enrollments, Instructors, Lecture Summaries, Students, and more** ensure comprehensive data management and relationships.

## Implementation

- **Requirements Gathering:** Focused on the needs of blind students.
- **System Design:** Ensured accessibility, security, and scalability.
- **Environment Setup:** Tools and environments like Supabase and TypeScript.
- **Backend and Frontend Development:** Developed RESTful APIs and accessible interfaces.
- **Challenges and Solutions:** Addressed accessibility and real-time data synchronization.

## Results and Discussion

- The system successfully meets its objectives by providing an inclusive educational environment and enhancing accessibility for blind students.

## Future Work

- Develop a dedicated mobile application.
- Implement a user feedback system.
- Integrate adaptive learning tools.
- Provide multimodal content delivery.

---

## Python Code for PDF Summarization

```python
import os
from PyPDF2 import PdfReader
from transformers import pipeline

def extract_text_from_pdf(file_path):
    text = []
    reader = PdfReader(file_path)
    for page in reader.pages:
        text.append(page.extract_text())
    return "\n".join(text)

def summarize_text(text, model_name="facebook/bart-large-cnn", max_words_per_summary=300):
    summarizer = pipeline("summarization", model=model_name)
    max_chunk_size = 1024  # max tokens for BART
    
    # Helper function to split text into chunks of a specified size
    def split_text_into_chunks(text, chunk_size):
        words = text.split()
        for i in range(0, len(words), chunk_size):
            yield ' '.join(words[i:i + chunk_size])
    
    # Split text into chunks
    text_chunks = list(split_text_into_chunks(text, max_words_per_summary))
    
    # Summarize each chunk
    summaries = []
    for chunk in text_chunks:
        summary = summarizer(chunk, max_length=max_words_per_summary, min_length=max_words_per_summary // 2, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    
    # Combine all summaries into a final summary
    final_summary = ' '.join(summaries)
    return final_summary

if __name__ == "__main__":
    pdf_path = "/content/Fine-Tuning_a_Transformer-Based_Language_Model_to_.pdf"
    text = extract_text_from_pdf(pdf_path)
    summary = summarize_text(text)
    print("Summary:")
    print(summary)
