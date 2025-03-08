
# Virtual Labeling

[Link to the Notebook](https://colab.research.google.com/drive/15BLlhxweXbDWCa0uIZDo5oGfuDlU19Do?usp=sharing)

## Authors

**Author 1 (name and surname):** Alan García Justel

**Author 1 (name and surname):** Julen Rodríguez 


## Questions in the assignment

**Looking at the images, why do you think it is possible to predict cell nuclei from their membrane labeling? Think about what requirements may be needed for this task or when it is not possible to learn such prediction.**

*Because it seems that nuclei's positions in the membrane-labeled image are darker spots than the membrane, this suggests that the nuclei create gaps or lower-intensity regions in the membrane signal.*

**Train a generative model to predict cell nuclei labeling from their membrane labeling in fluorescence microscopy images of Drosophila Melanogaster embryos. (This part is performed following the guidelines below).**

*The training was made taking a pretrained checkpoint and then fine-tuning it with the membrane labeling data for 10 epochs*

**Interpret the different accuracy metrics compiled along the notebook. For this, here are some questions to discuss within your team.**

- **What is the difference between SSIM, MSE, and LPIPS?**
    
    *SSIM, MSE, and LPIPS are three different metrics used to evaluate image similarity but with distinct approaches. MSE (Mean Squared Error) measures the average squared pixel-wise difference between corresponding pixels from source and target images, making it easy to compute but it isn't well-aligned with human perception. SSIM (Structural Similarity Index) improves upon MSE by considering structural information, luminance, and contrast, making it more perceptually relevant. However, it may still struggle with slight texture variations. LPIPS (Learned Perceptual Image Patch Similarity) is a deep learning-based metric that captures perceptual differences in images, making it the most human-aligned among the three. While MSE is useful for straightforward numerical comparison, SSIM and LPIPS provide more insightful assessments of image quality, especially when human perception matters.*
    
- **Are hallucinations an important issue in this case?**
    
    *Hallucinations refer to the generation of false or misleading details in AI-generated content. In this case, they are a significant issue, as the model may produce fake nuclei, leading to incorrect data for further analysis. Therefore, minimizing hallucinations is a crucial factor when developing these types of models.*
    
- **Are the previous metrics capable of identifying hallucinations?**
    
    *SSIM and MSE might fail to detect such hallucinations properly, as they focus on pixel-wise and structural differences rather than perceptual realism. LPIPS, being based on deep network features, could be more sensitive to hallucinated textures but might still struggle if the hallucinations are perceptually plausible. In this case, the LPIPS map between the target and predicted images makes it easy to identify areas where the model generates hallucinations, which are not as clearly detected with SSIM.*

**What would you take into consideration to determine whether this is a good or a bad method?**

*When evaluating a method for generating nucleus images from membrane images, several factors must be considered. The generated images should be visually realistic and accurately represent nuclei's structure, assessed through metrics like LPIPS, SSIM, and expert review. The method must preserve key biological features, such as shape, size, and boundaries, and align with ground truth annotations for reliable segmentation. It should also handle variations in membrane images (e.g., noise or lighting) and be computationally efficient for large datasets or real-time use.*

- **What actions would you propose to improve the results?**
    *We suggest actions like data augmentation with changes in size, orientation, contrast, and adding noise to make the model more robust. Including domain knowledge can help improve biological accuracy, and using post-processing methods can refine the results. Modifying loss functions to include perceptual loss will help the model focus on important features. Cross-validation and real-world annotations will ensure the model is reliable, and hybrid models can improve the accuracy of nucleus shape and boundaries. These strategies should improve the quality, accuracy, and generalizability of the generated nucleus images.*

