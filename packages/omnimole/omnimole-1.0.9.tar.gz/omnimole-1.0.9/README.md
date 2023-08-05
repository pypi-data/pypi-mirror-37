# Omnimole
This repository is for the image processing code used in the Omnium app.
The purpose of the app is to detect malignant skin lesions in hopes of
early diagnosis of skin cancer and melanoma.

### Authors
* Kyle Pierson
* John Lackey

## Pipeline
1. Resize
2. Histogram equalize
3. Histogram match
4. Denoise/filter hair
5. Enhance edges/moles
6. Register to average image
7. Segment skin
8. Detect moles
9. Match moles
