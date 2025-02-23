

Complexity is measured in FLOPs
1. Key to reduce FLOPs -> Grouped convolutions.
    - An especial case of Groupred Convolutions is Depthwise Convolutoin (Nº of groups = Nº of input channels)
    - Depthwise Convolutions have some properties:
        * Operates only in space
        * No mixed channels
        * It reduces the number of parameters
        * Some architectures: ResNet -> ResNext

2. How to add accuracy without increasing FLOPs? -> Squeeze-and-excitation (focusing on the important channels)
    - 1-step: squeeze
    - 2-step: excitation
    - 3-step: res-scaling
    - SENet

3. Balance between accuracy/FLOPs (Mobile Devices):
    - MobileNet (Depthwise)
    - MobileNetv2 (Depthwise + inverted bottleneck)
    - ShuffleNet (Randomly moving channels to mix them up)

4. NAS Models were designed to fcreate optimal architectures but are very expensive and just optimize FLOPs doesn't necessary means to 
    get more performance on the models.
    - EfficientNet-Bx (low FLOPs but very slow)

5. RegNet -> Searching efficient scalability (mainly through slighly manual changes or tweaks) 

