<h1 align="center">🌸 Flower</h1>
<p align="center">
  <img width="700" src="https://i.imgur.com/GtZ5RDO.png">
</p>


# About Flower
This script is currently working with 4 browsers. This project is alive and new browsers will be available in next commits.

Here list of available and possible available in future browsers:
| Browser            | Status                                |
| :----------------: | ------------------------------------- |
| Chrome             | ✅ Supported                         |
| Firefox            | ✅ Supported                         |
| Opera              | ✅ Supported                         |
| Opera GX           | ✅ Supported                         |
| Edge               | ❌ Will be supported in future       |
| Internet Explorer  | ❌ **Won't be supported**            |
| Yandex Browser     | ❌ Will be supported in future       |

# Installation

* Clone this repository
* Extract it
* Open cmd and execute few commands:
```
cd Downloads
cd flower
pip install -r requirements.txt
```

# Usage

Flower accepts few parameters.

| Parameter name    | Description                                         | Required |
| :---------------: | --------------------------------------------------- | :------: |
| **chrome**        | Flower will be able to work with Chrome             | No       |
| **firefox**       | Flower will be able to work with Firefox            | No       |
| **opera**         | Flower will be able to work with Opera              | No       |
| **operagx**       | Flower will be able to work with Opera GX           | No       |
| **type**          | Selects needed file format on output (txt or csv)   | Yes      |

Here an example how to run **Flower**:

```
python flower.py -chrome -type csv
```
