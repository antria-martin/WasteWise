# Waste Identification System with AI-Driven Sustainability Recommendations

An AI-powered mobile waste management system that combines **computer vision** and **large language models (LLMs)** to identify waste items and provide actionable sustainability recommendations for recycling, disposal, reuse, and upcycling.

---

## 1. Project Overview

Improper waste disposal often occurs because people are unable to correctly identify the type of waste they have or do not know the appropriate disposal method.

Existing waste-classification applications generally stop after identifying a broad waste category such as plastic, paper, glass, or metal. They provide limited guidance about what the user should actually do with the item.

This project addresses this limitation by combining:

1. **Computer Vision** — identifies the specific waste object and its broad waste category.
2. **Knowledge Mapping** — maps the identified object to a standardized waste category.
3. **AI Recommendation Engine** — uses verified waste information and an LLM to generate actionable sustainability recommendations.
4. **Flutter Mobile Application** — provides an intuitive interface for capturing/uploading waste images and displaying recommendations.

### Core concept

```text
User Image
    │
    ▼
Computer Vision
    │
    ├── Specific Object
    │       e.g. plastic_bottle
    │
    └── Waste Category
            e.g. plastic
    │
    ▼
Knowledge Mapping
    │
    ▼
LLM Recommendation Engine
    │
    ├── Recycling
    ├── Disposal
    ├── Reuse
    ├── Upcycling
    └── Safety Guidance
    │
    ▼
Flutter Mobile Application
```

---

# 2. Problem Statement

People frequently misclassify household waste and may not know whether an item should be recycled, reused, upcycled, composted, or disposed of as general waste.

Most existing computer-vision waste applications focus primarily on classification and do not provide sufficient **actionable, context-aware guidance** after identifying an item.

There is therefore a need for an intelligent system that can:

- identify a waste object from an image,
- determine its waste category,
- provide appropriate disposal/recycling instructions,
- suggest reuse and upcycling possibilities,
- and communicate the information in an accessible manner.

---

# 3. Project Objectives

The system aims to:

- Identify individual waste objects from images.
- Determine the broad waste category of the identified object.
- Provide reliable waste-management information.
- Generate recycling and disposal instructions.
- Suggest practical reuse ideas.
- Generate creative upcycling suggestions.
- Provide safety warnings where appropriate.
- Present the results through a mobile application.
- Evaluate both computer-vision performance and recommendation quality.

---

# 4. System Architecture

The system is divided into three major components.

```text
                         ┌───────────────────┐
                         │   Flutter Mobile  │
                         │       App         │
                         └─────────┬─────────┘
                                   │
                              Image Upload
                                   │
                                   ▼
                         ┌───────────────────┐
                         │    FastAPI        │
                         │     Backend       │
                         └─────────┬─────────┘
                                   │
                     ┌─────────────┴─────────────┐
                     │                           │
                     ▼                           ▼
             ┌───────────────┐           ┌───────────────┐
             │ Object Model  │           │ Category Model│
             │ MobileNetV3   │           │ MobileNetV3   │
             │    Small      │           │    Small      │
             └───────┬───────┘           └───────┬───────┘
                     │                           │
                     ▼                           ▼
              Specific Object             Waste Category
              plastic_bottle                 plastic
                     │                           │
                     └─────────────┬─────────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ Knowledge Mapping │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ AI Recommendation │
                         │      Engine       │
                         │   Knowledge Base  │
                         │       + LLM       │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         Sustainability Advice
                                   │
                                   ▼
                            Flutter Results
```

---

# 5. Three-Team-Member Division

## Member 1 — Mobile Application & Integration

Responsible for:

- Flutter application development
- UI/UX
- Camera integration
- Gallery/image upload
- Image preview
- API communication
- Loading/error handling
- Displaying classification results
- Displaying recommendations
- Final application integration
- APK/deployment

---

## Member 2 — Computer Vision & ML

Responsible for:

- Dataset preparation
- Dataset cleaning
- Image preprocessing
- Training the object-identification model
- Training the waste-category model
- Model evaluation
- TFLite conversion
- FastAPI computer-vision inference
- API response design

### Two independent models are used:

**Model 1 — Object Identification**

```text
Input Image
     ↓
MobileNetV3-Small
     ↓
Specific Object
     ↓
plastic_bottle
```

**Model 2 — Waste Category**

```text
Input Image
     ↓
MobileNetV3-Small
     ↓
Broad Category
     ↓
plastic
```

Both models receive the **same original image** independently.

---

## Member 3 — AI Recommendation & Knowledge Engine

Responsible for:

- Waste knowledge database
- Object-to-category knowledge mapping
- Disposal rules
- Recycling instructions
- Reuse suggestions
- Upcycling suggestions
- Safety rules
- LLM integration
- Prompt engineering
- Recommendation evaluation

The LLM should not independently invent disposal rules.

Instead:

```text
Verified Knowledge
       +
Object
       +
Category
       ↓
      LLM
       ↓
Natural-language recommendation
```

---

# 6. Computer Vision Design

## 6.1 Why Two Models?

The system separates:

### Fine-grained object identification

Answers:

> "What specific object is this?"

Example:

```text
plastic_bottle
glass_bottle
metal_can
cardboard_box
battery
mobile_phone
```

### Broad category classification

Answers:

> "What waste category does it belong to?"

Example:

```text
plastic
glass
metal
paper
cardboard
organic
general_waste
```

This separation allows the recommendation engine to receive both the **specific object** and the **broad waste category**.

---

# 7. Object Identification Model

## Model

**MobileNetV3-Small**

## Dataset

Primary dataset:

**TACO — Trash Annotations in Context**

TACO contains waste objects in real-world contexts with object annotations.

Because MobileNetV3-Small is being used as an image classifier rather than an object detector, TACO's annotated objects should be **cropped using their bounding-box annotations** before being used for classification.

```text
TACO Image
     ↓
Bounding Box
     ↓
Object Crop
     ↓
MobileNetV3-Small
```

### Additional data

Custom images will be collected to represent the conditions expected in the actual mobile application.

Custom images should include variation in:

- background,
- lighting,
- orientation,
- distance,
- object shape,
- object brand,
- object condition.

### Potential object classes

The final class list should be determined based on dataset availability and project scope.

Examples:

```text
plastic_bottle
glass_bottle
plastic_bag
plastic_container
metal_can
glass_jar
cardboard_box
newspaper
paper_cup
food_waste
battery
mobile_phone
laptop
```

Only classes supported reliably by the dataset should be included.

---

# 8. Waste Category Model

## Model

**MobileNetV3-Small**

## Primary Dataset

**TrashNet**

TrashNet provides common waste categories including:

```text
cardboard
glass
metal
paper
plastic
trash
```

## Additional Dataset

An enhanced garbage-classification dataset may be used to increase the amount and diversity of category-level training data.

Possible additional categories include:

```text
paper
cardboard
biological
metal
plastic
glass
batteries
trash
```

Dataset labels should be normalized into the project's final category taxonomy before training.

---

# 9. Category Taxonomy

A proposed final category set is:

```text
plastic
glass
metal
paper
cardboard
organic
general_waste
```

If required by the recommendation engine, additional categories may be introduced:

```text
e_waste
hazardous
```

The final taxonomy must be fixed before training.

---

# 10. Custom Image Collection

Custom images are important because public datasets may not accurately represent the photographs users will take through the mobile application.

The custom dataset should contain realistic smartphone photographs.

## Recommended target

Approximately:

**100–200+ images per category**

More images can be collected for difficult or highly variable categories.

### Plastic

Examples:

- water bottles
- soft-drink bottles
- shampoo bottles
- detergent bottles
- plastic bags
- food containers
- takeaway containers
- plastic cups
- wrappers
- packaging

### Paper

Examples:

- newspapers
- printer paper
- notebooks
- magazines
- receipts
- paper bags
- envelopes
- loose sheets

### Cardboard

Examples:

- shipping boxes
- cereal boxes
- packaging cartons
- corrugated cardboard
- tissue boxes
- small cartons

### Glass

Examples:

- glass bottles
- sauce bottles
- jam jars
- glass food containers
- glass jars

### Metal

Examples:

- beverage cans
- food cans
- tins
- aluminium cans
- metal containers
- foil

### Organic

Examples:

- banana peels
- orange peels
- apple cores
- vegetable scraps
- leftover food
- eggshells
- fruit waste

### General Waste

Examples should consist of items that do not clearly belong to the supported recyclable/organic categories.

---

# 11. Image Variation

Custom images should intentionally contain variation in:

### Background

- table
- desk
- floor
- kitchen counter
- outdoor surfaces
- different backgrounds

### Lighting

- daylight
- indoor lighting
- low-light conditions
- shadows

### Orientation

- upright
- sideways
- tilted
- front
- back

### Distance

- close
- medium
- farther away

### Condition

- clean
- slightly dirty
- crushed
- damaged

The goal is to simulate real mobile-app usage.

---

# 12. Dataset Split

Recommended:

```text
70% → Training
15% → Validation
15% → Testing
```

The test set must remain separate until final evaluation.

When multiple photographs of the same physical object exist, those photographs should preferably remain within the same split.

For example:

```text
Bottle A
 ├── photo 1
 ├── photo 2
 ├── photo 3
 └── photo 4

→ TRAIN
```

rather than placing different photos of the same physical object into both training and testing datasets.

---

# 13. MobileNetV3-Small Training

Transfer learning should be used rather than training from scratch.

```text
ImageNet-pretrained MobileNetV3-Small
             ↓
Remove original classifier
             ↓
Add project-specific classifier
             ↓
Train on waste dataset
```

Example architecture:

```text
224 × 224 × 3 image
        ↓
MobileNetV3-Small backbone
        ↓
Feature extraction
        ↓
Global Average Pooling
        ↓
Dense layer
        ↓
Dropout
        ↓
Final classification layer
        ↓
Softmax
```

The exact input size and preprocessing must match the model's training configuration.

---

# 14. Training Strategy

Because the project uses transfer learning:

### Stage 1

Freeze the MobileNetV3-Small backbone and train the new classification head.

```text
Backbone → Frozen
Classifier → Trainable
```

### Stage 2 (optional)

If additional performance is required, unfreeze some later backbone layers and fine-tune with a small learning rate.

```text
Early layers → Frozen
Later layers → Trainable
Classifier → Trainable
```

---

# 15. Data Augmentation

Moderate augmentation should be applied to training images.

Potential transformations:

- horizontal flipping
- small rotations
- zoom
- cropping
- brightness variation
- contrast variation

Augmentation should remain realistic for waste objects.

---

# 16. Class Imbalance

Class distributions should be checked before training.

If one category contains significantly more images than another, possible solutions include:

- class weighting,
- oversampling,
- additional custom images,
- augmentation.

The goal is to prevent the model from becoming biased toward the majority category.

---

# 17. Computer Vision Evaluation

The category model should be evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix

Per-class metrics should also be reported.

Example:

```text
Category       Precision   Recall   F1
-----------------------------------------
Plastic           --        --      --
Glass             --        --      --
Metal             --        --      --
Paper             --        --      --
Cardboard         --        --      --
Organic           --        --      --
General Waste     --        --      --
```

The actual values will be populated after testing.

---

# 18. Model Testing

Testing should include both:

### Public test data

Used to measure standard model performance.

### Real custom photographs

Completely new photographs should be captured using a phone and used as an application-oriented evaluation set.

Example:

```text
Plastic bottle
      ↓
PLASTIC — 0.94

Glass bottle
      ↓
GLASS — 0.92

Metal can
      ↓
METAL — 0.96
```

The custom evaluation set should contain images that were not used during training.

---

# 19. TFLite Deployment

Once training is complete, each model is exported independently.

```text
Object Model
     ↓
Trained Keras/TensorFlow Model
     ↓
TensorFlow Lite Converter
     ↓
object_model.tflite
```

```text
Category Model
     ↓
Trained Keras/TensorFlow Model
     ↓
TensorFlow Lite Converter
     ↓
category_model.tflite
```

The backend performs inference using the two `.tflite` files.

Optional optimization such as float16 quantization can be considered after obtaining a working model.

---

# 20. Backend Structure

The CV backend uses **Python + FastAPI**.

Recommended structure:

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── models/
│   │   ├── object_model.tflite
│   │   └── category_model.tflite
│   │
│   ├── labels/
│   │   ├── object_labels.txt
│   │   └── category_labels.txt
│   │
│   ├── inference/
│   │   ├── object_classifier.py
│   │   └── category_classifier.py
│   │
│   ├── preprocessing/
│   │   └── image.py
│   │
│   ├── mappings/
│   │   └── object_to_category.py
│   │
│   └── routes/
│       └── prediction.py
│
├── requirements.txt
└── README.md
```

---

# 21. Backend Model Loading

The TFLite models should be loaded **once when the FastAPI application starts**, rather than loading them for every request.

```text
FastAPI starts
     ↓
Load object_model.tflite
     ↓
Load category_model.tflite
     ↓
Keep interpreters in memory
     ↓
Process requests
```

This reduces unnecessary inference latency.

---

# 22. Backend Inference Pipeline

Both models receive the original uploaded image.

```text
                 Original Image
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
       Object Model        Category Model
             │                   │
             ▼                   ▼
     plastic_bottle            plastic
          0.94                   0.91
```

The models should not be chained together.

The category model should not receive the object model's output as its input.

---

# 23. Confidence and Logical Compatibility Verification

The object model identifies the specific item, while the category model independently predicts its broad waste category.

The system should first check whether either model's confidence is below the minimum confidence threshold. A recommended threshold is 0.60 or 0.70, depending on validation results.

If either prediction falls below the threshold, the item should be treated as unidentifiable rather than being assigned to the default `general_waste` category.

```python
CONFIDENCE_THRESHOLD = 0.70

if (
    object_confidence < CONFIDENCE_THRESHOLD
    or category_confidence < CONFIDENCE_THRESHOLD
):
    result = {
        "identifiable": False,
        "message": "The item could not be identified confidently. Please upload a clearer image or ensure that the image contains a trash item."
    }
```

This confidence check must be performed before applying any fallback category. The system must not automatically classify a low-confidence prediction as `general_waste`.

If both predictions meet the confidence threshold, the system should perform a logical compatibility check.

The system should maintain a deterministic compatibility table that defines which object classes are valid for each category.

Example:

```python
OBJECT_CATEGORY_COMPATIBILITY = {
    "plastic_bottle": {"plastic"},
    "plastic_bag": {"plastic"},
    "plastic_container": {"plastic"},

    "glass_bottle": {"glass"},
    "glass_jar": {"glass"},

    "metal_can": {"metal"},

    "cardboard_box": {"cardboard"},
    "newspaper": {"paper"},

    "food_waste": {"organic"},

    "battery": {"hazardous"},
    "mobile_phone": {"e_waste"},
    "laptop": {"e_waste"}
}
```

The backend compares the object model's predicted object with the category model's predicted category.

```python
predicted_object = "plastic_bottle"
predicted_category = "plastic"

compatible_categories = OBJECT_CATEGORY_COMPATIBILITY.get(
    predicted_object,
    set()
)

is_compatible = predicted_category in compatible_categories
```

Example of a compatible prediction:

```text
Object model: plastic_bottle
Category model: plastic
Result: compatible
```

Example of an incompatible prediction:

```text
Object model: plastic_bottle
Category model: glass
Result: incompatible
```

The compatibility check does not replace either model and does not determine the category itself. It only verifies whether the two independent predictions agree logically.

The API should return the verification result:

```json
{
    "identifiable": true,
    "object": "plastic_bottle",
    "object_confidence": 0.94,
    "category": "plastic",
    "category_confidence": 0.91,
    "compatible": true
}
```

If either confidence score is below the threshold, the API should return an unidentifiable response:

```json
{
    "identifiable": false,
    "object": null,
    "object_confidence": 0.42,
    "category": null,
    "category_confidence": 0.55,
    "compatible": false,
    "message": "The item could not be identified confidently. Please upload a clearer image or ensure that the image contains a trash item."
}
```

If the predictions are incompatible despite having sufficient confidence, the system should avoid generating a confident recommendation. It may instead:

- request another image,
- display an uncertainty message,
- ask the user to confirm the item,
- or use a clearly defined fallback rule only if the project requires one.

The system should not assign `general_waste` solely because the model confidence is low or because the predictions are incompatible.

The compatibility table and confidence threshold should be maintained as part of the system's configuration and should not rely on the LLM.

# 24. Model Consistency Checking

The backend can compare:

```text
Object model category
        vs.
Category model prediction
```

This check should only be performed after both model confidence scores meet the configured confidence threshold.

Example:

```text
Object:
plastic_bottle — 0.94

Category:
plastic — 0.91

→ Consistent and identifiable
```

If either confidence score is below the threshold:

```text
Object:
unknown — 0.42

Category:
general_waste — 0.55

→ Unidentifiable
```

The system should return an unidentifiable response instead of treating the item as `general_waste`.

If both predictions have sufficient confidence but disagree:

```text
Object:
glass_bottle — 0.82

Category:
plastic — 0.76

→ Model disagreement
```

The backend can return a consistency flag so the recommendation engine can avoid generating a confident recommendation and request user confirmation or another image.

---

# 25. API Response

The main computer-vision endpoint is:

```http
POST /predict
```

Input:

```text
multipart/form-data
image = photo.jpg
```

Example response:

```json
{
    "object": "plastic_bottle",
    "object_confidence": 0.94,
    "category": "plastic",
    "category_confidence": 0.91,
    "mapped_category": "plastic",
    "consistent": true
}
```

This JSON is the handoff between the computer-vision component and the recommendation component.

---

# 26. Optional Top-K Predictions

The API may also expose the top predictions.

Example:

```json
{
    "object": {
        "label": "glass_bottle",
        "confidence": 0.71,
        "top_predictions": [
            ["glass_bottle", 0.71],
            ["plastic_bottle", 0.21],
            ["glass_jar", 0.05]
        ]
    }
}
```

This allows the recommendation engine to distinguish between high-confidence and uncertain predictions.

---

# 27. Recommendation Engine

The recommendation component receives:

```text
Object
Category
Confidence
Knowledge Base Information
```

Example:

```json
{
    "object": "plastic_bottle",
    "category": "plastic",
    "confidence": 0.94
}
```

The recommendation system can then provide:

- recommended disposal method,
- recycling preparation,
- reuse ideas,
- upcycling ideas,
- safety warnings.

---

# 28. Hybrid Recommendation Architecture

The recommendation engine should use both **rules/knowledge** and an **LLM**.

```text
CV Prediction
      ↓
Knowledge Base
      ↓
Verified Waste Information
      ↓
Rule Engine
      ↓
LLM
      ↓
Natural-Language Recommendation
```

### Rules/knowledge base handle:

- material
- recycling eligibility
- disposal requirements
- hazardous waste
- safety restrictions
- preparation instructions

### LLM handles:

- natural-language explanation
- reuse suggestions
- upcycling ideas
- personalization
- conversational presentation

This reduces the risk of the LLM generating unsupported disposal information.

---

# 29. Example End-to-End Flow

### User uploads a photo

```text
Plastic bottle
```

### Object model

```text
plastic_bottle
confidence = 0.94
```

### Category model

```text
plastic
confidence = 0.91
```

### Knowledge mapping

```text
plastic_bottle → plastic
```

### Recommendation engine

The knowledge base supplies verified information.

### LLM

Generates a user-friendly response:

```text
Plastic Bottle

Recommended action:
Recycle

Before recycling:
1. Empty the bottle.
2. Rinse it if necessary.
3. Allow it to dry.
4. Follow local recycling guidelines.

Reuse idea:
Use the bottle as a small planter.

Upcycling idea:
Turn it into a hanging planter.

Avoid:
Do not burn the plastic.
```

---

# 30. Latency Considerations

The two MobileNetV3-Small models should be relatively lightweight.

The knowledge mapping is effectively negligible compared with model inference.

The LLM API call is expected to be the most variable component because it depends on:

- network latency,
- API response time,
- model used,
- prompt size.

Therefore the system should distinguish between:

### CV latency

```text
Image preprocessing
+
Object inference
+
Category inference
+
Mapping
```

and:

### End-to-end latency

```text
Upload
+
CV inference
+
Mapping
+
LLM request
+
Response
```

Both can be reported separately.

---

# 31. Technology Stack

| Component             | Technology                        |
| --------------------- | --------------------------------- |
| Mobile application    | Flutter / Dart                    |
| Backend               | Python / FastAPI                  |
| Computer Vision       | TensorFlow / Keras                |
| CV architecture       | MobileNetV3-Small                 |
| Image processing      | OpenCV / Pillow                   |
| Model deployment      | TensorFlow Lite                   |
| Object dataset        | TACO                              |
| Category dataset      | TrashNet + additional public data |
| Custom data           | Self-collected smartphone images  |
| Recommendation engine | LLM + knowledge base              |
| Database              | SQLite / Firebase                 |
| API                   | REST                              |

---

# 32. Current Project Responsibility — Member 2

The computer-vision member is responsible for:

```text
Dataset
   ↓
Cleaning
   ↓
Label normalization
   ↓
Train/Val/Test split
   ↓
Preprocessing
   ↓
MobileNetV3-Small
   ↓
Training
   ↓
Evaluation
   ↓
TFLite conversion
   ↓
FastAPI inference
   ↓
JSON response
```

### Final deliverables

- Object identification dataset
- Category classification dataset
- Data preprocessing scripts
- Trained object model
- Trained category model
- Evaluation results
- Confusion matrices
- `.tflite` models
- Label files
- FastAPI inference endpoint
- API documentation

---

# 33. Current Development Plan

## Phase 1 — Category Model

```text
TrashNet
   +
Custom images
   ↓
Label normalization
   ↓
Dataset split
   ↓
MobileNetV3-Small
   ↓
Training
   ↓
Evaluation
```

## Phase 2 — Object Model

```text
TACO
   ↓
Extract annotated object crops
   +
Custom images
   ↓
Label normalization
   ↓
Dataset split
   ↓
MobileNetV3-Small
   ↓
Training
   ↓
Evaluation
```

## Phase 3 — TFLite

```text
Object model → object_model.tflite
Category model → category_model.tflite
```

## Phase 4 — FastAPI

```text
POST /predict
       ↓
Object inference
       +
Category inference
       ↓
Knowledge mapping
       ↓
JSON response
```

## Phase 5 — Integration

```text
Flutter
   ↓
FastAPI
   ↓
CV predictions
   ↓
Recommendation engine
   ↓
LLM
   ↓
Flutter
```

---

# 34. Key Design Decisions

### Decision 1 — Two independent CV models

The system uses separate models for:

- specific object identification,
- broad waste category classification.

### Decision 2 — Both models process the original image

They operate independently rather than passing predictions between models.

### Decision 3 — Deterministic category mapping

Object-to-category mapping is handled using a knowledge mapping layer rather than asking the LLM to determine the category.

### Decision 4 — TFLite deployment

The trained models are converted to `.tflite` for lightweight inference.

### Decision 5 — FastAPI backend

FastAPI provides a clean REST interface between the Flutter application and the ML models.

### Decision 6 — Hybrid recommendation system

Verified waste knowledge and rules are combined with an LLM rather than relying exclusively on generative AI.

---

# 35. Example Final System

```text
                    ┌─────────────┐
                    │   Flutter   │
                    │     App     │
                    └──────┬──────┘
                           │
                         Image
                           │
                           ▼
                  ┌─────────────────┐
                  │     FastAPI     │
                  └────────┬────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
      ┌───────────────┐         ┌───────────────┐
      │ Object Model  │         │ Category Model│
      │ MobileNetV3-S │         │ MobileNetV3-S │
      └───────┬───────┘         └───────┬───────┘
              │                         │
              ▼                         ▼
       plastic_bottle                 plastic
              │                         │
              └────────────┬────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Knowledge Base  │
                  │ + Rule Engine   │
                  └────────┬────────┘
                           │
                           ▼
                     ┌───────────┐
                     │    LLM    │
                     └─────┬─────┘
                           │
                           ▼
              ┌────────────────────────┐
              │ Sustainability Advice │
              ├────────────────────────┤
              │ Recycling             │
              │ Disposal              │
              │ Reuse                 │
              │ Upcycling             │
              │ Safety                │
              └───────────┬────────────┘
                          │
                          ▼
                    Flutter UI
```

---

# 36. Project Goal

The final system should transform:

> **"What is this waste?"**

into:

> **"What is this item, what waste category does it belong to, and what should I do with it?"**

The central contribution is therefore an **end-to-end intelligent waste management system combining visual identification with actionable, knowledge-grounded AI sustainability recommendations.**
