# Evaluating Efficient CV Algorithms for Form Processing



## Introduction

The chemistry department at SLU currently uses paper-based Scantron sheets (Form 95945) for exams, which are graded using aging physical machines. Our project aims to digitize this grading process through software that automates scanning and data extraction. While our existing method achieves 100% accuracy, its complexity poses challenges for scalability, especially when introducing support for custom-designed sheets.

This document evaluates existing computer vision (CV) algorithms known for efficiency in form processing. We compare the top three algorithms against our current method, focusing on accuracy, processing speed, resource usage, and implementation complexity. Additionally, we explore the potential of using Convolutional Neural Networks (CNNs) for form processing and discuss strategies to overcome challenges related to dataset size and variability.

---

## Current Method Overview

Our current processing pipeline involves:

1. **Image Alignment using ORB Feature Matching:**
   - Uses ORB (Oriented FAST and Rotated BRIEF) to detect keypoints and compute descriptors.
   - Aligns scanned images to a template via homography transformation.

2. **ROI Extraction via Contour Detection:**
   - Detects specific markers (contours) to identify regions of interest (ROIs) for bubbles and student IDs.

3. **Bubble Detection using Pixel Counting:**
   - Analyzes each bubble's pixel intensity to determine if it's filled.

**Strengths:**

- High accuracy (near 100%).
- Robust to minor variations in scanning.

**Weaknesses:**

- Complex implementation.
- Computationally intensive due to feature matching.
- Difficult to scale for custom forms with different layouts.

---

## Top 3 Alternative CV Algorithms

### 1. Edge Detection with Perspective Transformation

**Overview:**

This method uses edge detection to identify the boundaries of the form and applies a perspective transformation to align the image.

**How It Works:**

- **Edge Detection:** Utilizes algorithms like the Canny Edge Detector to find edges in the image.
- **Contour Detection:** Finds contours and identifies the largest quadrilateral, assuming it's the form.
- **Perspective Transformation:** Maps the detected corners to a predefined coordinate system to align the image.

**Pros:**

- **Simplified Alignment:** Eliminates the need for complex feature matching.
- **Faster Processing:** Reduces computational load.
- **Adaptable:** Can be recalibrated for different form sizes and layouts.

**Cons:**

- **Sensitivity to Image Quality:** Requires clear edges; poor scans may reduce accuracy.
- **Less Robust to Occlusions:** Markings or damage near edges can affect detection.

**Comparison to Current Method:**

- **Accuracy:** Comparable if scans are of good quality.
- **Processing Speed:** Faster due to simpler computations.
- **Resource Usage:** Lower CPU and memory consumption.
- **Implementation Complexity:** Easier to implement and maintain.

---

### 2. Grid-Based Approach for Bubble Detection

**Overview:**

After aligning the form, this method defines a grid over the image where each cell corresponds to a bubble. Bubble detection is then performed based on pixel intensity within these predefined cells.

**How It Works:**

- **Grid Definition:** Establishes a grid mapping to the expected bubble positions.
- **Bubble Detection:** Analyzes the pixel intensity or counts the number of dark pixels in each cell to determine if a bubble is filled.

**Pros:**

- **High Efficiency:** Eliminates the need for contour detection and feature matching.
- **Scalability:** Easily adaptable to different forms by adjusting grid parameters.
- **Simplified Processing:** Reduces the algorithm to basic image thresholding and pixel analysis.

**Cons:**

- **Alignment Dependency:** Requires precise alignment; misalignment can lead to incorrect readings.
- **Less Robust to Variations:** May struggle with forms that have significant distortions or scanning artifacts.

**Comparison to Current Method:**

- **Accuracy:** Slightly lower if alignment is imperfect, but can be improved with calibration.
- **Processing Speed:** Significantly faster due to reduced computational steps.
- **Resource Usage:** Minimal resource requirements.
- **Implementation Complexity:** Simple to implement and modify.

---

## Consideration of CNNs for Form Processing

### Overview

Convolutional Neural Networks (CNNs) have demonstrated exceptional capabilities in image recognition and classification tasks. Applying CNNs to form processing can potentially improve robustness and accuracy, especially in handling variations in form designs and scanning conditions.

### How It Works

- **Model Training:** A CNN is trained on labeled images of bubbles and form elements to learn features that distinguish filled bubbles from empty ones.
- **Bubble Detection:** The trained CNN scans the form image and predicts the status of each bubble.
- **Form Alignment and ROI Extraction:** CNNs can be used to detect form boundaries and regions of interest without relying on traditional feature matching or edge detection.

### Pros

- **Robustness to Variations:** CNNs can handle variations in form designs, distortions, and noise in scanned images.
- **Automated Feature Extraction:** Eliminates the need for manual feature engineering; the CNN learns relevant features during training.
- **Adaptability:** Capable of generalizing to new form layouts with additional training.

### Cons

- **Data Requirements:** Requires a large and diverse dataset for effective training.
- **Computational Resources:** Training and inference can be computationally intensive.
- **Implementation Complexity:** More complex to develop, train, and maintain compared to traditional methods.

### Addressing Data Limitations

#### Synthetic Data Generation

To overcome the challenge of limited datasets, synthetic data can be generated to augment the training set.

- **Technique:** Use software to create artificial Scantron sheets with varying styles, bubble fill patterns, and scanning artifacts.
- **Variations Introduced:**
  - **Form Layouts:** Alter positions of bubbles, question numbers, and ID sections.
  - **Bubble Fill Patterns:** Simulate different ways students fill bubbles (e.g., fully filled, partially filled, crossed out).
  - **Scanning Artifacts:** Add noise, blur, rotation, scaling, and contrast variations to mimic real-world scanning conditions.
- **Tools:**
  - **Image Processing Libraries:** Use libraries like OpenCV and PIL to programmatically generate and modify images.
  - **Data Augmentation Frameworks:** Leverage frameworks that support augmentation techniques (e.g., Keras’ ImageDataGenerator, Albumentations).

#### Data Augmentation Techniques

- **Geometric Transformations:** Apply rotations, shifts, zooms, and flips.
- **Photometric Adjustments:** Alter brightness, contrast, and add noise.
- **Elastic Transformations:** Slightly distort images to simulate paper bending or scanning irregularities.
- **Occlusions:** Add random lines or marks to simulate stray pen marks or stains.

### Implementation Strategy

1. **Dataset Preparation:**

   - **Collect Real Samples:** Gather as many scanned forms as possible to serve as a base dataset.
   - **Generate Synthetic Data:** Augment the dataset with artificially generated images covering a wide range of variations.

2. **Model Design:**

   - **Choose Architecture:** Opt for a lightweight CNN architecture suitable for the task (e.g., MobileNet, custom shallow CNN).
   - **Output Format:** Design the model to output probabilities for each bubble being filled.

3. **Training:**

   - **Labeling Data:** Ensure that all training images are accurately labeled.
   - **Validation Set:** Set aside a portion of data for validation to monitor overfitting.
   - **Training Parameters:** Adjust learning rates, batch sizes, and epochs based on performance.

4. **Evaluation:**

   - **Accuracy Metrics:** Use metrics like precision, recall, and F1-score for evaluation.
   - **Inference Speed:** Test processing times to ensure the method meets performance requirements.

5. **Integration:**

   - **Pipeline Integration:** Incorporate the CNN into the processing pipeline, replacing or supplementing existing methods.
   - **Fallback Mechanisms:** Implement checks to fall back on traditional methods if the CNN's confidence is low.

### Comparison to Current Method

- **Accuracy:** Potentially higher, especially in handling ambiguous cases.
- **Processing Speed:** Slower per image due to model inference time but can be optimized.
- **Resource Usage:** Higher computational requirements; may need GPU acceleration.
- **Implementation Complexity:** More complex due to the need for model training and maintenance.

---

## Comparative Analysis

| Criteria                | Current Method                        | Edge Detection & Perspective Transformation | Grid-Based Approach                | CNN-Based Method                   |
|-------------------------|---------------------------------------|---------------------------------------------|------------------------------------|-------------------------------------|
| **Accuracy**            | Near 100%                             | High (with good image quality)              | Moderate to High (alignment-dependent)|High (with sufficient training data) |
| **Processing Speed**    | Slow (feature matching is intensive)  | Fast                                        | Very Fast                          | Moderate (can be optimized)         |
| **Resource Usage**      | High CPU and memory usage             | Low                                         | Very Low                           | High (requires GPU for training)    |
| **Implementation Complexity** | Complex (hard to maintain and scale) | Simple                                      | Very Simple                   | Complex (requires ML expertise)     |
| **Scalability**         | Difficult (complex for custom forms)  | Easy (adjust corner detection)              | Easy (adjust grid parameters)      | Easy (with additional training)     |

---

## Conclusion and Recommendations

### **Recommendation: Edge Detection with Perspective Transformation**

Given the balance between accuracy, processing speed, resource usage, and implementation complexity, adopting the **Edge Detection with Perspective Transformation** method is recommended.

**Justification:**

- **Improved Efficiency:** Faster processing and lower resource consumption compared to the current method.
- **Maintainable:** Simpler codebase, making it easier to implement and maintain.
- **Scalable:** Can be adapted to different form layouts with minimal adjustments.

### **Consideration of CNN-Based Method**

While CNNs offer potential benefits in robustness and adaptability, the increased complexity and resource requirements make it a secondary consideration.

**Conditions for Adoption:**

- **Availability of Data:** If we can generate a sufficiently large and diverse dataset through synthetic generation and augmentation.
- **Resource Allocation:** If computational resources (e.g., GPUs) and expertise in machine learning are available.
- **Long-Term Scalability:** If we anticipate frequent changes in form designs and need a highly adaptable system.

---

## References

- **OpenCV Documentation:**
  - [Edge Detection (Canny)](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html)
  - [Perspective Transformation](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html)
  - [ArUco Marker Detection](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html)

- **Tutorials:**
  - [Data Augmentation Techniques](https://machinelearningmastery.com/how-to-configure-image-data-augmentation-when-training-deep-learning-neural-networks/)

---

