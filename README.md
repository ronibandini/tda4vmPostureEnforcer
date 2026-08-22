# 🧍‍♂️👁️ TDA4VM Posture Enforcer

**An edge-AI computer-vision prototype that recognizes correct and incorrect working posture.**

TDA4VM Posture Enforcer explores a practical industrial computer-vision problem:

> Can a camera continuously recognize whether a worker is using a machine with the expected posture and turn that recognition into a physical action?

The reference experiment focuses on repetitive leather-working operations involving hard pressing.

A USB camera observes the operator. An **Edge Impulse FOMO object-detection model** classifies the visible posture as:

```text
ok
```

or:

```text
notok
```

The model runs locally on a **Texas Instruments SK-TDA4VM**. A Python script parses the inference output and controls a relay through the board's GPIO header.

```text
             Worker
                │
                ▼
          USB webcam
                │
                ▼
     ┌─────────────────────┐
     │ Texas Instruments   │
     │     SK-TDA4VM       │
     │                     │
     │ Edge Impulse Linux  │
     │ FOMO model          │
     └──────────┬──────────┘
                │
          ┌─────┴─────┐
          ▼           ▼
        `ok`       `notok`
          │           │
          │           ▼
          │      posture1.py
          │           │
          │           ▼
          │        GPIO 18
          │           │
          │           ▼
          │         Relay
          │
          ▼
     Continue monitoring
```

The repository is a compact companion to the complete **Edge Impulse Expert Network** tutorial, where dataset creation, TDA4VM configuration, model training, deployment, GPIO setup, and relay integration are documented in detail.

---

## ✨ Features

- 👁️ Real-time camera-based posture recognition
- 🧠 Edge Impulse Machine Learning
- 🎯 FOMO object detection
- ⚡ Texas Instruments SK-TDA4VM
- 🚀 Hardware-accelerated edge inference
- 📷 Logitech USB webcam support
- 🏷️ Two posture labels: `ok` and `notok`
- 📦 Public Edge Impulse model
- 🐍 Python inference-output parser
- 🔌 GPIO-controlled relay
- 📴 Local inference without cloud video streaming
- 📊 Bounding-box confidence output

---

## 🧠 Concept

Traditional programming works well when a condition can be expressed using clear rules.

For posture recognition, a rule such as:

```text
if shoulder_x < 32
and head_y > 41
and arm_angle < 70:
    posture = bad
```

would be brittle.

Real images vary because of:

- body proportions
- clothing
- lighting
- background
- camera position
- machine position
- movement
- partial occlusion
- different workers

Instead, the project trains a computer-vision model from examples.

```text
Examples of correct posture
            +
Examples of incorrect posture
            │
            ▼
       Edge Impulse
            │
            ▼
       FOMO model
            │
            ▼
New camera image
            │
       ┌────┴─────┐
       ▼          ▼
      `ok`      `notok`
```

---

# 🏭 Reference use case

The original experiment was created around a leather-working process involving repeated manual pressing.

The task requires the operator to maintain a particular body position while repeatedly using a machine.

The project investigates whether computer vision can automate the observation step:

```text
Supervisor demonstrates
expected posture
       │
       ▼
Capture examples
       │
       ▼
Train model
       │
       ▼
Machine monitors
future operation
```

---

# ⚡ Texas Instruments SK-TDA4VM

The project runs on the:

**Texas Instruments SK-TDA4VM Starter Kit**

The board is designed specifically for embedded computer vision and Edge AI.

Official information:

**[SK-TDA4VM — Texas Instruments](https://www.ti.com/tool/SK-TDA4VM)**

The underlying **TDA4VM** SoC includes:

- Dual 64-bit Arm Cortex-A72 up to 2 GHz
- C7x DSP
- Deep-learning matrix accelerator
- Up to **8 TOPS** of 8-bit AI performance
- Vision-processing accelerators
- Depth and motion processing
- PowerVR GPU
- Multiple Arm Cortex-R5F cores
- Hardware video acceleration

Processor documentation:

**[TDA4VM — Texas Instruments](https://www.ti.com/product/TDA4VM)**

---

## 🧠 Why the TDA4VM?

The board provides considerably more vision-processing capability than a small microcontroller.

The project benefits from:

```text
camera input
+
Linux
+
Python
+
Edge Impulse Linux Runner
+
TI deep-learning acceleration
+
GPIO
```

on the same platform.

The SK-TDA4VM also supports multiple camera interfaces, making multi-view posture analysis a possible extension.

---

# 🧰 Hardware

The reference build uses:

| Qty | Component | Purpose |
|---:|---|---|
| 1 | **Texas Instruments SK-TDA4VM** | Edge AI inference |
| 1 | **Logitech C270, C920 or C922 USB webcam** | Image acquisition |
| 1 | **1-channel relay module** | Physical output |
| 1 | microSD card | TDA4VM Linux image |
| 1 | Ethernet cable | SSH / network access |
| 1 | 5 V / 3 A USB-C power supply | Board power |

The repository also includes:

```text
TDA4VMGpioPinout.jpg
```

as a GPIO-header reference.

---

# 📷 Camera

The documented setup supports conventional USB webcams such as:

```text
Logitech C270
Logitech C920
Logitech C922
```

The camera should be positioned so that the relevant working posture remains visible during the complete task.

A fixed camera mount is strongly recommended.

Changes in:

```text
camera angle
distance
height
field of view
```

can affect model behavior if those conditions were not represented in the training data.

---

# 🧠 Edge Impulse project

The complete public Machine Learning project is available in Edge Impulse Studio:

**[Posture Detection — Public Edge Impulse Project](https://studio.edgeimpulse.com/public/222158/latest)**

It can be cloned instead of rebuilding the model from scratch.

---

# 📊 Dataset

The reference dataset was intentionally small.

Approximately:

```text
50 images → correct posture
50 images → incorrect posture
```

were collected.

Some images were discarded because they contained:

- only background
- non-representative machine states
- unsuitable frames

Each usable image was annotated with a bounding box.

Labels:

```text
ok
notok
```

---

## 📱 Data acquisition

Although Edge Impulse can capture images directly from connected hardware, the reference dataset was collected using an Android phone.

The project used **Open Camera** because it supports:

```text
repeated photos
+
configurable intervals
+
small image resolution
```

This allowed images to be collected at the actual workplace without moving the TDA4VM setup.

---

# 🏷️ Bounding-box labeling

The Edge Impulse project uses:

```text
Bounding Boxes
```

as the labeling method.

Each training image contains a box around the worker and one of two labels:

```text
ok
```

or:

```text
notok
```

Conceptually:

```text
┌────────────────────────────┐
│                            │
│        ┌──────────┐        │
│        │  worker  │        │
│        │          │        │
│        └──────────┘        │
│             `ok`           │
│                            │
└────────────────────────────┘
```

or:

```text
┌────────────────────────────┐
│                            │
│      ┌────────────┐        │
│      │   worker   │        │
│      │            │        │
│      └────────────┘        │
│           `notok`          │
│                            │
└────────────────────────────┘
```

---

# 🧩 Impulse configuration

The reference Edge Impulse impulse uses:

```text
Image Data
   │
   ▼
96 × 96 pixels
Resize: Fit shortest axis
   │
   ▼
Image processing
   │
   ▼
Object Detection
   │
   ▼
FOMO
```

Training configuration:

```text
Training cycles: 60
Learning rate:   0.001
Data augmentation: enabled
Model: FOMO
```

---

# 🎯 FOMO

The project uses **FOMO — Faster Objects, More Objects**, Edge Impulse's lightweight object-detection architecture.

Instead of returning only:

```text
image = bad posture
```

the model can return localized detections:

```json
{
  "height": 8,
  "label": "notok",
  "value": 0.71,
  "width": 8,
  "x": 64,
  "y": 72
}
```

The result includes:

| Field | Meaning |
|---|---|
| `label` | `ok` or `notok` |
| `value` | Detection confidence |
| `x` | Detection location |
| `y` | Detection location |
| `width` | Bounding-cell width |
| `height` | Bounding-cell height |

---

# 📊 Reference training result

The original experiment reported:

```text
F1 score: 71.4%
```

and:

```text
Incorrect-posture detection rate: 100%
```

for the small reference dataset.

These values belong to that specific training run.

---

# 🧪 Inference examples

## No posture detected

```text
boundingBoxes 2ms. []
boundingBoxes 1ms. []
```

---

## Correct posture

Example:

```text
boundingBoxes 1ms.
[
  {
    "height": 8,
    "label": "ok",
    "value": 0.5057658553123474,
    "width": 8,
    "x": 48,
    "y": 24
  }
]
```

---

## Incorrect posture

Example:

```text
boundingBoxes 1ms.
[
  {
    "height": 8,
    "label": "notok",
    "value": 0.7100046873092651,
    "width": 8,
    "x": 64,
    "y": 72
  }
]
```

The runner continuously generates these detections from the USB camera stream.

---

# 🔌 Relay output

A single-channel relay provides the physical-output portion of the experiment.

The documented GPIO is:

```text
GPIO 18
```

The demonstration architecture is:

```text
FOMO prediction
      │
      ▼
posture1.py
      │
      ▼
GPIO 18
      │
      ▼
Relay
      │
      ▼
External load / test machine
```

The relay converts the Machine Learning result into an observable physical action.

---

# 🧩 40-pin expansion header

The SK-TDA4VM includes a:

```text
40-pin
2 × 20
2.54 mm
```

expansion header.

It exposes interfaces including:

- GPIO
- I²C
- SPI
- I²S
- UART
- PWM

The interface signals use:

```text
3.3 V logic
```

The repository includes:

[`TDA4VMGpioPinout.jpg`](TDA4VMGpioPinout.jpg)

as a practical pinout reference created during development.

---

# ⚙️ Enabling the expansion header

Expansion-header GPIO was disabled by default in the Linux configuration used by the original project.

After initially obtaining no GPIO output, the solution was to modify:

```text
/run/media/mmcblk0p1/uenv.txt
```

and add:

```text
name_overlays=k3-j721e-edgeai-apps.dtbo k3-j721e-sk-rpi-exp-header.dtbo
```

After rebooting with that overlay, GPIO control became available.

> This reflects the Processor SDK configuration used by the original project. Current Texas Instruments SDK releases may use different device-tree or overlay procedures, so check the documentation for the image you install.

---

# 🐍 GPIO test

The original GPIO test uses the Raspberry Pi-compatible GPIO interface:

```python
import RPi.GPIO as GPIO
import time

output_pin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(output_pin, GPIO.OUT)

GPIO.output(output_pin, GPIO.HIGH)
time.sleep(3)
GPIO.output(output_pin, GPIO.LOW)
```

This provides a simple hardware test before combining relay control with Machine Learning.

---

# 🐍 `posture1.py`

The repository's main source file is:

```text
posture1.py
```

Its role is to bridge:

```text
Machine Learning prediction
```

and:

```text
GPIO action
```

The script parses the output produced by the Edge Impulse Linux Runner, identifies the posture label, and changes the relay state accordingly.

```text
edge-impulse-linux-runner
        │
        ▼
boundingBoxes output
        │
        ▼
posture1.py
        │
   ┌────┴────┐
   ▼         ▼
 `ok`     `notok`
   │         │
   ▼         ▼
relay      relay
state      state
```

The important architectural point is that the inference model and the physical action remain separate components.

This makes it possible to replace the relay action with something else without retraining the model.

---

# 🔄 Alternative outputs

Instead of switching a relay, the same recognition event could trigger:

```text
warning light
buzzer
screen message
industrial stack light
MQTT event
database log
Telegram message
supervisor notification
PLC input
```

The ML model answers:

```text
What posture is visible?
```

while the application decides:

```text
What should happen next?
```

---

# 💻 TDA4VM operating system

The original build uses the Texas Instruments Processor SDK Linux image for the SK-TDA4VM.

Current official downloads:

**[PROCESSOR-SDK-LINUX-SK-TDA4VM](https://www.ti.com/tool/download/PROCESSOR-SDK-LINUX-SK-TDA4VM)**

Flash the provided:

```text
.wic.xz
```

image to a microSD card.

The original tutorial used an older release than the current Texas Instruments SDK, so filenames, included packages, login defaults, and device-tree configuration may differ today.

---

# 🌐 Connecting to the board

The reference development workflow uses:

```text
SK-TDA4VM
   │
   ▼
Ethernet
   │
   ▼
Router
   │
   ▼
SSH / SFTP
```

Find the board's IP address through the router's DHCP-client list and connect over SSH.

The historical SDK used:

```text
User: root
Password: empty
```

Do not assume current images use the same credentials.

If an image ships with permissive defaults, secure it before connecting the board to an untrusted network.

---

# 📦 Install Edge Impulse Linux

The reference setup installs the Linux tools with:

```bash
npm install -g --unsafe-perm edge-impulse-linux
```

Then launches the model with explicit TI acceleration:

```bash
edge-impulse-linux-runner \
  --force-engine tidl \
  --force-target runner-linux-aarch64-tda4vm
```

On the first run, authenticate with Edge Impulse and select the posture-detection project.

---

# 📷 Camera preview

Once the Edge Impulse Linux Runner is active, the original setup exposes a camera-preview page on:

```text
http://<TDA4VM-IP>:4912
```

For example:

```text
http://192.168.1.50:4912
```

Use this preview to verify:

- worker visibility
- camera angle
- lighting
- framing
- model predictions

before relying on the parser.

---

# 📂 Installing `posture1.py`

Transfer:

```text
posture1.py
```

to:

```text
/opt/edge_ai_apps
```

using SFTP or another file-transfer method.

Then run:

```bash
cd /opt/edge_ai_apps
python3 posture1.py
```

The script then connects the model output to the GPIO relay action.

---

# 📁 Repository structure

```text
tda4vmPostureEnforcer/
├── LICENSE
├── README.md
├── TDA4VMGpioPinout.jpg
└── posture1.py
```

### `posture1.py`

Python glue code connecting Edge Impulse inference output to GPIO relay control.

### `TDA4VMGpioPinout.jpg`

Reference image for the SK-TDA4VM 40-pin expansion header.

### `README.md`

Original repository description and Edge Impulse project link.

### `LICENSE`

MIT License.

---

# 🚀 Quick start

## 1. Clone the repository

```bash
git clone https://github.com/ronibandini/tda4vmPostureEnforcer.git
cd tda4vmPostureEnforcer
```

---

## 2. Clone the ML model

Open:

**[Public Edge Impulse project](https://studio.edgeimpulse.com/public/222158/latest)**

and clone it into your own Edge Impulse account.

---

## 3. Install the TDA4VM Linux image

Download the current:

**[TI Processor SDK for SK-TDA4VM](https://www.ti.com/tool/download/PROCESSOR-SDK-LINUX-SK-TDA4VM)**

and flash the `.wic.xz` image to a microSD card.

---

## 4. Connect the webcam

Attach a compatible USB camera such as:

```text
Logitech C270
Logitech C920
Logitech C922
```

---

## 5. Enable the GPIO header if required

For the historical SDK configuration, add:

```text
name_overlays=k3-j721e-edgeai-apps.dtbo k3-j721e-sk-rpi-exp-header.dtbo
```

to:

```text
/run/media/mmcblk0p1/uenv.txt
```

Reboot the board.

Check the current TI SDK documentation before applying this to a newer image.

---

## 6. Test GPIO 18

Test the relay output independently before introducing the model.

Do this with a harmless low-voltage test load first.

---

## 7. Install Edge Impulse

```bash
npm install -g --unsafe-perm edge-impulse-linux
```

---

## 8. Run inference

```bash
edge-impulse-linux-runner \
  --force-engine tidl \
  --force-target runner-linux-aarch64-tda4vm
```

Verify the model through:

```text
http://<deviceIP>:4912
```

---

## 9. Run the posture controller

Copy:

```text
posture1.py
```

to:

```text
/opt/edge_ai_apps
```

and execute:

```bash
python3 posture1.py
```

---

# 🧪 Rebuilding the model

To create a model for another task or workplace:

```text
1. Capture examples of accepted posture

2. Capture examples of unacceptable posture

3. Include different workers

4. Include realistic clothing

5. Include normal background variation

6. Label bounding boxes

7. Split train/test data

8. Train FOMO

9. Evaluate false positives

10. Evaluate false negatives

11. Deploy to TDA4VM

12. Validate using unseen workers
```

A production-quality system should use substantially more data than the reference proof of concept.

---

# 🔬 Ideas for extending the project

1. **📷 Multi-camera posture detection** — combine front and side views using the TDA4VM's multi-camera capabilities to reduce ambiguity.

2. **⏱️ Temporal filtering** — require several consecutive `notok` detections before generating an alert or control event, reducing reactions to single-frame false positives.

3. **📊 Event logging** — save confidence, timestamps, posture duration, and machine state for later process analysis and model improvement.

---

# 📰 External references

## 🗞️ Edge Impulse — Straightening Out Posture in the Workplace

Edge Impulse published a dedicated article by **Nick Bild** on July 3, 2023.

The feature covers:

- leather-work posture
- Texas Instruments SK-TDA4VM
- USB webcam
- approximately 50 good and 50 bad posture images
- bounding-box labeling
- Edge Impulse FOMO
- 71%+ F1 score
- local edge inference
- privacy advantages of on-device vision
- relay integration
- possible multi-camera extensions

**[Straightening Out Posture in the Workplace — Edge Impulse](https://www.edgeimpulse.com/blog/straightening-out-posture-in-the-workplace/)**

---

## 🧠 Edge Impulse Expert Network

The complete technical guide is part of the **Edge Impulse Expert Network**:

**[Correct Posture Detection and Enforcement — Texas Instruments TDA4VM](https://docs.edgeimpulse.com/projects/expert-network/ti-tda4vm-posture-detection)**

The guide documents the full workflow from TDA4VM setup through relay control.

---

## 🧪 Public Edge Impulse project

The complete trained project is publicly cloneable:

**[Posture Detection — Edge Impulse Studio](https://studio.edgeimpulse.com/public/222158/latest)**

---

## 📚 Edge Impulse project index

The project is listed in the Edge Impulse Expert Network's **Computer Vision Projects** collection alongside other TDA4VM deployments.

**[Edge Impulse Expert Network project list](https://docs.edgeimpulse.com/projects/expert-network/project-list)**

---

## 📰 Wevolver

The project is also referenced in Wevolver's article on high-performance microprocessors for Edge AI computer vision.

It appears as an example of posture detection and immediate physical feedback running on a Texas Instruments vision platform.

**[Building Robust Edge AI Computer Vision Applications with High-Performance Microprocessors — Wevolver](https://www.wevolver.com/article/building-robust-edge-ai-computer-vision-applications-with-high-performance-microprocessors)**

---

# 📕 Contracultura Maker

More projects, technical experiments, embedded AI systems, unusual machines, and Maker Counterculture are collected in:

**[Contracultura Maker — book](https://bandini.medium.com/libro-de-contracultura-maker-94d1bb0d951c)**

---

# 📚 Useful references

- **[Texas Instruments SK-TDA4VM](https://www.ti.com/tool/SK-TDA4VM)**
- **[Texas Instruments TDA4VM](https://www.ti.com/product/TDA4VM)**
- **[Processor SDK Linux for SK-TDA4VM](https://www.ti.com/tool/download/PROCESSOR-SDK-LINUX-SK-TDA4VM)**
- **[Edge Impulse](https://edgeimpulse.com/)**
- **[Public posture model](https://studio.edgeimpulse.com/public/222158/latest)**
- **[Complete Edge Impulse tutorial](https://docs.edgeimpulse.com/projects/expert-network/ti-tda4vm-posture-detection)**
- **[FOMO object detection](https://docs.edgeimpulse.com/studio/projects/learning-blocks/blocks/object-detection/fomo)**
- **[Open Camera](https://opencamera.org.uk/)**

---

# 🔗 You may also be interested in...

Other projects by **Roni Bandini** using Edge Impulse and Texas Instruments edge-AI hardware.

## 👁️⚙️ Visual Anomaly

**Real-time visual anomaly detection for industrial inspection using Edge Impulse FOMO-AD on the Texas Instruments SK-TDA4VM.**

It uses the same hardware family for a different industrial computer-vision problem.

**[github.com/ronibandini/visualAnomaly](https://github.com/ronibandini/visualAnomaly)**

---

## 🤟🧠 ASL Trainer

**American Sign Language training system using Machine Learning and Texas Instruments edge-AI hardware.**

Another project combining real-time computer vision with a physical learning/application workflow.

**[github.com/ronibandini/ASLTrainer](https://github.com/ronibandini/ASLTrainer)**

---

## 🎙️⚡ RUBIK Pi Audio Classification

**Real-time glass-break sound classification using Edge Impulse and GPIO output on the Thundercomm RUBIK Pi 3.**

Like Posture Enforcer, it converts an Edge Impulse inference result into an immediate physical GPIO action.

**[github.com/ronibandini/Rubik-Pi-AudioClassification](https://github.com/ronibandini/Rubik-Pi-AudioClassification)**

---

# ⚠️ Deployment considerations


## ML false positives and false negatives

The model is probabilistic.

Possible outcomes include:

```text
bad posture classified as good
good posture classified as bad
no detection
multiple detections
```

A production system should therefore consider:

- confidence thresholds
- temporal filtering
- manual override
- event logging
- watchdogs
- fail-safe behavior
- independent safety mechanisms

---

# 📜 License

TDA4VM Posture Enforcer is released under the **MIT License**.

See [`LICENSE`](LICENSE) for details.

---

# 👤 Author

**Roni Bandini**

Maker, AI developer, electronic artist and writer.

- 🐙 GitHub: [@ronibandini](https://github.com/ronibandini)
- 💼 LinkedIn: [Roni Bandini](https://www.linkedin.com/in/ronibandini/)
- 📸 Instagram: [@ronibandini](https://www.instagram.com/ronibandini/)
- 🐦 X: [@RoniBandini](https://x.com/RoniBandini)
- ✍️ Medium: [bandini.medium.com](https://bandini.medium.com/)
- 🛠️ Hackster: [Roni Bandini](https://www.hackster.io/roni-bandini)
- 🔧 Hackaday.io: [Roni Bandini](https://hackaday.io/ronibandini)

Buenos Aires, Argentina.
