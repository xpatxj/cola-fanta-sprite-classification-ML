{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyPARFsJXSTgHA7UJ8sfGozM",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/xpatxj/cola-fanta-sprite-classification/blob/main/cola-fanta-sprite.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "uIVbOU5bhIkc",
        "outputId": "b13446a9-b59b-4035-ec5a-e88a58bd6e39"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: gdown in /usr/local/lib/python3.10/dist-packages (4.6.6)\n",
            "Collecting gdown\n",
            "  Downloading gdown-4.7.1-py3-none-any.whl (15 kB)\n",
            "Requirement already satisfied: filelock in /usr/local/lib/python3.10/dist-packages (from gdown) (3.13.1)\n",
            "Requirement already satisfied: requests[socks] in /usr/local/lib/python3.10/dist-packages (from gdown) (2.31.0)\n",
            "Requirement already satisfied: six in /usr/local/lib/python3.10/dist-packages (from gdown) (1.16.0)\n",
            "Requirement already satisfied: tqdm in /usr/local/lib/python3.10/dist-packages (from gdown) (4.66.1)\n",
            "Requirement already satisfied: beautifulsoup4 in /usr/local/lib/python3.10/dist-packages (from gdown) (4.11.2)\n",
            "Requirement already satisfied: soupsieve>1.2 in /usr/local/lib/python3.10/dist-packages (from beautifulsoup4->gdown) (2.5)\n",
            "Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.10/dist-packages (from requests[socks]->gdown) (3.3.2)\n",
            "Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.10/dist-packages (from requests[socks]->gdown) (3.6)\n",
            "Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.10/dist-packages (from requests[socks]->gdown) (2.0.7)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.10/dist-packages (from requests[socks]->gdown) (2023.11.17)\n",
            "Requirement already satisfied: PySocks!=1.5.7,>=1.5.6 in /usr/local/lib/python3.10/dist-packages (from requests[socks]->gdown) (1.7.1)\n",
            "Installing collected packages: gdown\n",
            "  Attempting uninstall: gdown\n",
            "    Found existing installation: gdown 4.6.6\n",
            "    Uninstalling gdown-4.6.6:\n",
            "      Successfully uninstalled gdown-4.6.6\n",
            "Successfully installed gdown-4.7.1\n",
            "Downloading...\n",
            "From (uriginal): https://drive.google.com/uc?id=1BpccrvnDWO4XcOSQz08Xc4rGYQR7gOLq\n",
            "From (redirected): https://drive.google.com/uc?id=1BpccrvnDWO4XcOSQz08Xc4rGYQR7gOLq&confirm=t&uuid=76f063e6-274e-40ec-97ee-d7d2954497ce\n",
            "To: /content/ai.zip\n",
            "100% 36.2M/36.2M [00:00<00:00, 50.5MB/s]\n"
          ]
        }
      ],
      "source": [
        "#instalacja pakietu gdown\n",
        "!pip install -U --no-cache-dir gdown --pre\n",
        "#usuwanie i tworzenie pustego katalogu data\n",
        "!rm -rf data && mkdir data\n",
        "#pobieranie zip-a ze zdjęciami\n",
        "!gdown 1BpccrvnDWO4XcOSQz08Xc4rGYQR7gOLq -O ai.zip\n",
        "#rozpakowywanie pliku data.zip do katalogu data\n",
        "!unzip -q ai.zip -d data"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import matplotlib.pyplot as plt\n",
        "import numpy as np\n",
        "import PIL\n",
        "import tensorflow as tf\n",
        "import glob\n",
        "import os\n",
        "import xml.etree.ElementTree as ET\n",
        "\n",
        "from tensorflow import keras\n",
        "from tensorflow.keras import layers\n",
        "from tensorflow.keras.models import Sequential"
      ],
      "metadata": {
        "id": "-vlVZe6uhM2-"
      },
      "execution_count": 4,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "tree = ET.parse('/content/data/ai/annotations.xml')\n",
        "root = tree.getroot()\n",
        "\n",
        "for child in root.iter('image'):\n",
        "    image_name = child.attrib['name'].replace('ai/', '')\n",
        "    image_label = child[0].attrib['label']\n",
        "\n",
        "    if not os.path.isdir(f'/content/data/ai/{image_label}'):\n",
        "        os.mkdir(f'/content/data/ai/{image_label}')\n",
        "\n",
        "    os.replace(f'/content/data/ai/{image_name}', f'/content/data/ai/{image_label}/{image_name}')\n"
      ],
      "metadata": {
        "id": "o4CJk9rUhNdY"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "cola_count = len(list(glob.glob('data/**/cola/*.jpg')))\n",
        "fanta_count = len(list(glob.glob('data/**/fanta/*.jpg')))\n",
        "sprite_count = len(list(glob.glob('data/**/sprite/*.jpg')))\n",
        "print(f'{cola_count} examples of cola, {fanta_count} examples of fanta and {sprite_count} examples of sprite to train')"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "GIi58kVRijWa",
        "outputId": "40d3cdfb-2f2b-46d3-a79f-ea1168dd0869"
      },
      "execution_count": 6,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "27 examples of cola, 26 examples of fanta and 27 examples of sprite to train\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "cola = list(glob.glob('data/ai/cola/*'))\n",
        "PIL.Image.open(str(cola[3]))"
      ],
      "metadata": {
        "id": "yaxtYEvPjcOQ"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "batch_size = 32\n",
        "class_count = 3\n",
        "\n",
        "img_height = 64\n",
        "img_width = 64"
      ],
      "metadata": {
        "id": "0GEZbtbgjy-P"
      },
      "execution_count": 9,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "train_ds = tf.keras.utils.image_dataset_from_directory(\n",
        "  'data/ai',\n",
        "  validation_split=0.2,\n",
        "  subset='training',\n",
        "  seed=123,\n",
        "  image_size=(img_height, img_width),\n",
        "  batch_size=batch_size)\n",
        "\n",
        "val_ds = tf.keras.utils.image_dataset_from_directory(\n",
        "  'data/ai',\n",
        "  validation_split=0.2,\n",
        "  subset='validation',\n",
        "  seed=123,\n",
        "  image_size=(img_height, img_width),\n",
        "  batch_size=batch_size)"
      ],
      "metadata": {
        "id": "xNXgnNOwj7qM",
        "outputId": "7238cce0-f6c1-4909-e700-d5638bc23879",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "execution_count": 10,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Found 80 files belonging to 3 classes.\n",
            "Using 64 files for training.\n",
            "Found 80 files belonging to 3 classes.\n",
            "Using 16 files for validation.\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "class_names = train_ds.class_names\n",
        "print(f'class names: {class_names}')"
      ],
      "metadata": {
        "id": "Oz5kzNmKkWYX",
        "outputId": "371caea3-7266-4b42-bc02-07b07fc7744c",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "execution_count": 11,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "class names: ['cola', 'fanta', 'sprite']\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=tf.data.AUTOTUNE)\n",
        "val_ds = val_ds.cache().prefetch(buffer_size=tf.data.AUTOTUNE)"
      ],
      "metadata": {
        "id": "kUU0fy-pk8KQ"
      },
      "execution_count": 12,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "model = Sequential([\n",
        "  layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),\n",
        "  layers.Conv2D(16, 3, padding='same', activation='relu'),\n",
        "  layers.MaxPooling2D(),\n",
        "  layers.Conv2D(32, 3, padding='same', activation='relu'),\n",
        "  layers.MaxPooling2D(),\n",
        "  layers.Conv2D(64, 3, padding='same', activation='relu'),\n",
        "  layers.MaxPooling2D(),\n",
        "  layers.Flatten(),\n",
        "  layers.Dense(128, activation='relu'),\n",
        "  layers.Dense(class_count)\n",
        "])"
      ],
      "metadata": {
        "id": "DxmhBWwzk-Ow"
      },
      "execution_count": 13,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "model.compile(optimizer='adam',\n",
        "              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),\n",
        "              metrics=['accuracy'])\n",
        "model.summary()"
      ],
      "metadata": {
        "id": "FVb_l2BmlAUB",
        "outputId": "03782e14-83a2-4af7-b825-beda545d016f",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "execution_count": 14,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Model: \"sequential\"\n",
            "_________________________________________________________________\n",
            " Layer (type)                Output Shape              Param #   \n",
            "=================================================================\n",
            " rescaling (Rescaling)       (None, 64, 64, 3)         0         \n",
            "                                                                 \n",
            " conv2d (Conv2D)             (None, 64, 64, 16)        448       \n",
            "                                                                 \n",
            " max_pooling2d (MaxPooling2  (None, 32, 32, 16)        0         \n",
            " D)                                                              \n",
            "                                                                 \n",
            " conv2d_1 (Conv2D)           (None, 32, 32, 32)        4640      \n",
            "                                                                 \n",
            " max_pooling2d_1 (MaxPoolin  (None, 16, 16, 32)        0         \n",
            " g2D)                                                            \n",
            "                                                                 \n",
            " conv2d_2 (Conv2D)           (None, 16, 16, 64)        18496     \n",
            "                                                                 \n",
            " max_pooling2d_2 (MaxPoolin  (None, 8, 8, 64)          0         \n",
            " g2D)                                                            \n",
            "                                                                 \n",
            " flatten (Flatten)           (None, 4096)              0         \n",
            "                                                                 \n",
            " dense (Dense)               (None, 128)               524416    \n",
            "                                                                 \n",
            " dense_1 (Dense)             (None, 3)                 387       \n",
            "                                                                 \n",
            "=================================================================\n",
            "Total params: 548387 (2.09 MB)\n",
            "Trainable params: 548387 (2.09 MB)\n",
            "Non-trainable params: 0 (0.00 Byte)\n",
            "_________________________________________________________________\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "epochs=20\n",
        "history = model.fit(\n",
        "  train_ds,\n",
        "  validation_data=val_ds,\n",
        "  epochs=epochs\n",
        ")"
      ],
      "metadata": {
        "id": "eNvgL1rClCNW",
        "outputId": "553f19c6-64ff-48af-8360-79db12b35ec4",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "execution_count": 15,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Epoch 1/20\n",
            "2/2 [==============================] - 8s 3s/step - loss: 1.2629 - accuracy: 0.2656 - val_loss: 1.1699 - val_accuracy: 0.1875\n",
            "Epoch 2/20\n",
            "2/2 [==============================] - 0s 147ms/step - loss: 1.0999 - accuracy: 0.4531 - val_loss: 1.0628 - val_accuracy: 0.6250\n",
            "Epoch 3/20\n",
            "2/2 [==============================] - 0s 142ms/step - loss: 1.0476 - accuracy: 0.5000 - val_loss: 1.0399 - val_accuracy: 0.8125\n",
            "Epoch 4/20\n",
            "2/2 [==============================] - 0s 136ms/step - loss: 1.0108 - accuracy: 0.9062 - val_loss: 0.9981 - val_accuracy: 0.8125\n",
            "Epoch 5/20\n",
            "2/2 [==============================] - 0s 145ms/step - loss: 0.9462 - accuracy: 0.8594 - val_loss: 0.9606 - val_accuracy: 0.5625\n",
            "Epoch 6/20\n",
            "2/2 [==============================] - 0s 136ms/step - loss: 0.8463 - accuracy: 0.8125 - val_loss: 0.8625 - val_accuracy: 0.6250\n",
            "Epoch 7/20\n",
            "2/2 [==============================] - 0s 142ms/step - loss: 0.7203 - accuracy: 0.8906 - val_loss: 0.7314 - val_accuracy: 0.8125\n",
            "Epoch 8/20\n",
            "2/2 [==============================] - 0s 151ms/step - loss: 0.5806 - accuracy: 0.9062 - val_loss: 0.6091 - val_accuracy: 0.7500\n",
            "Epoch 9/20\n",
            "2/2 [==============================] - 0s 141ms/step - loss: 0.4436 - accuracy: 0.9219 - val_loss: 0.4330 - val_accuracy: 0.9375\n",
            "Epoch 10/20\n",
            "2/2 [==============================] - 0s 147ms/step - loss: 0.3126 - accuracy: 0.9375 - val_loss: 0.3668 - val_accuracy: 0.8125\n",
            "Epoch 11/20\n",
            "2/2 [==============================] - 0s 137ms/step - loss: 0.2118 - accuracy: 0.9531 - val_loss: 0.3622 - val_accuracy: 0.8125\n",
            "Epoch 12/20\n",
            "2/2 [==============================] - 0s 168ms/step - loss: 0.1538 - accuracy: 0.9844 - val_loss: 0.2904 - val_accuracy: 0.8750\n",
            "Epoch 13/20\n",
            "2/2 [==============================] - 0s 146ms/step - loss: 0.1045 - accuracy: 0.9844 - val_loss: 0.1727 - val_accuracy: 0.9375\n",
            "Epoch 14/20\n",
            "2/2 [==============================] - 0s 146ms/step - loss: 0.0695 - accuracy: 0.9844 - val_loss: 0.1556 - val_accuracy: 1.0000\n",
            "Epoch 15/20\n",
            "2/2 [==============================] - 0s 139ms/step - loss: 0.0478 - accuracy: 0.9844 - val_loss: 0.2384 - val_accuracy: 0.8125\n",
            "Epoch 16/20\n",
            "2/2 [==============================] - 0s 144ms/step - loss: 0.0314 - accuracy: 1.0000 - val_loss: 0.1688 - val_accuracy: 0.9375\n",
            "Epoch 17/20\n",
            "2/2 [==============================] - 0s 143ms/step - loss: 0.0163 - accuracy: 1.0000 - val_loss: 0.1007 - val_accuracy: 1.0000\n",
            "Epoch 18/20\n",
            "2/2 [==============================] - 0s 145ms/step - loss: 0.0123 - accuracy: 1.0000 - val_loss: 0.0854 - val_accuracy: 1.0000\n",
            "Epoch 19/20\n",
            "2/2 [==============================] - 0s 166ms/step - loss: 0.0063 - accuracy: 1.0000 - val_loss: 0.1030 - val_accuracy: 0.9375\n",
            "Epoch 20/20\n",
            "2/2 [==============================] - 0s 146ms/step - loss: 0.0044 - accuracy: 1.0000 - val_loss: 0.1187 - val_accuracy: 0.9375\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "acc = history.history['accuracy']\n",
        "val_acc = history.history['val_accuracy']\n",
        "\n",
        "loss = history.history['loss']\n",
        "val_loss = history.history['val_loss']\n",
        "\n",
        "epochs_range = range(epochs)\n",
        "\n",
        "plt.figure(figsize=(8, 8))\n",
        "plt.subplot(1, 2, 1)\n",
        "plt.plot(epochs_range, acc, label='Training Accuracy')\n",
        "plt.plot(epochs_range, val_acc, label='Validation Accuracy')\n",
        "plt.legend(loc='lower right')\n",
        "plt.title('Training and Validation Accuracy')\n",
        "\n",
        "plt.subplot(1, 2, 2)\n",
        "plt.plot(epochs_range, loss, label='Training Loss')\n",
        "plt.plot(epochs_range, val_loss, label='Validation Loss')\n",
        "plt.legend(loc='upper right')\n",
        "plt.title('Training and Validation Loss')\n",
        "plt.show()"
      ],
      "metadata": {
        "id": "F0AwJzzqlFD-",
        "outputId": "0ccabb33-7ebc-4f5a-c92b-09b6ae4a827b",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 699
        }
      },
      "execution_count": 16,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<Figure size 800x800 with 2 Axes>"
            ],
            "image/png": "iVBORw0KGgoAAAANSUhEUgAAAp8AAAKqCAYAAAB8XzUWAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjcuMSwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy/bCgiHAAAACXBIWXMAAA9hAAAPYQGoP6dpAADiA0lEQVR4nOzdd3xUZfb48c/MJJn0HpIAgYTQO9IEC6gogrKCrqKiCAquLNhYV2VVUHThuz9FXV0V14YNO2IBqSsqTTqidAiEkkICpNeZ+/vjzp0kpE2fSXLer1demdzcufeZGIeT5zznPDpFURSEEEIIIYTwAL23ByCEEEIIIVoOCT6FEEIIIYTHSPAphBBCCCE8RoJPIYQQQgjhMRJ8CiGEEEIIj5HgUwghhBBCeIwEn0IIIYQQwmMk+BRCCCGEEB4jwacQQgghhPAYCT5tNGnSJJKTkx167tNPP41Op3PtgHzMsWPH0Ol0LFq0yOP31ul0PP3009avFy1ahE6n49ixY40+Nzk5mUmTJrl0PM78rgghbCPvyQ2T9+Qq8p7se5p88KnT6Wz6WLdunbeH2uI98MAD6HQ6Dh8+XO85TzzxBDqdjt9++82DI7Pf6dOnefrpp9m1a5e3h1Knffv2odPpCAwM5Pz5894ejmhB5D256ZD3ZPfS/gB44YUXvD0Un+Pn7QE468MPP6zx9QcffMDq1atrHe/WrZtT93nrrbcwm80OPffJJ5/k8ccfd+r+zcGECRN49dVXWbx4MbNnz67znE8++YRevXrRu3dvh+9z5513cuutt2I0Gh2+RmNOnz7NM888Q3JyMn379q3xPWd+V1zlo48+IiEhgXPnzvHll18yZcoUr45HtBzyntx0yHuy8JYmH3zecccdNb7evHkzq1evrnX8QsXFxQQHB9t8H39/f4fGB+Dn54efX5P/UTtt8ODBdOzYkU8++aTON7pNmzaRlpbG//3f/zl1H4PBgMFgcOoaznDmd8UVFEVh8eLF3H777aSlpfHxxx/7bPBZVFRESEiIt4chXEjek5sOeU8W3tLk0+62GD58OD179mT79u1cfvnlBAcH849//AOAb775huuuu47WrVtjNBpJTU3l2WefxWQy1bjGhWtGqk+n//e//yU1NRWj0cjAgQPZunVrjefWtb5Ip9MxY8YMli5dSs+ePTEajfTo0YMVK1bUGv+6desYMGAAgYGBpKam8uabb9q8ZumXX37h5ptvpl27dhiNRpKSknj44YcpKSmp9fpCQ0M5deoUY8eOJTQ0lLi4OB555JFaP4vz588zadIkIiIiiIyM5K677rI5tTthwgT279/Pjh07an1v8eLF6HQ6brvtNsrLy5k9ezb9+/cnIiKCkJAQLrvsMn788cdG71HX+iJFUXjuuedo27YtwcHBXHHFFfzxxx+1nnv27FkeeeQRevXqRWhoKOHh4YwaNYrdu3dbz1m3bh0DBw4EYPLkydY0ora2qq71RUVFRfztb38jKSkJo9FIly5deOGFF1AUpcZ59vxe1GfDhg0cO3aMW2+9lVtvvZWff/6ZkydP1jrPbDbz73//m169ehEYGEhcXBzXXnst27Ztq3HeRx99xKBBgwgODiYqKorLL7+cVatW1Rhz9fVdmgvXbmn/XX766Sf++te/0qpVK9q2bQvA8ePH+etf/0qXLl0ICgoiJiaGm2++uc41YufPn+fhhx8mOTkZo9FI27ZtmThxIjk5ORQWFhISEsKDDz5Y63knT57EYDAwf/58G3+Swl3kPVnek1vSe3JjsrOzueeee4iPjycwMJA+ffrw/vvv1zrv008/pX///oSFhREeHk6vXr3497//bf1+RUUFzzzzDJ06dSIwMJCYmBguvfRSVq9e7bKxukqL+dMvNzeXUaNGceutt3LHHXcQHx8PqP9ThIaGMnPmTEJDQ/nf//7H7Nmzyc/P5/nnn2/0uosXL6agoIC//OUv6HQ6/t//+3/ceOONHD16tNG/ttavX8+SJUv461//SlhYGK+88go33XQT6enpxMTEALBz506uvfZaEhMTeeaZZzCZTMydO5e4uDibXvcXX3xBcXEx06ZNIyYmhi1btvDqq69y8uRJvvjiixrnmkwmRo4cyeDBg3nhhRdYs2YNCxYsIDU1lWnTpgHqG8YNN9zA+vXrue++++jWrRtff/01d911l03jmTBhAs888wyLFy/moosuqnHvzz//nMsuu4x27dqRk5PD22+/zW233cbUqVMpKCjgnXfeYeTIkWzZsqVWWqUxs2fP5rnnnmP06NGMHj2aHTt2cM0111BeXl7jvKNHj7J06VJuvvlmUlJSyMrK4s0332TYsGHs3buX1q1b061bN+bOncvs2bO59957ueyyywAYOnRonfdWFIU//elP/Pjjj9xzzz307duXlStX8ve//51Tp07x0ksv1Tjflt+Lhnz88cekpqYycOBAevbsSXBwMJ988gl///vfa5x3zz33sGjRIkaNGsWUKVOorKzkl19+YfPmzQwYMACAZ555hqeffpqhQ4cyd+5cAgIC+PXXX/nf//7HNddcY/PPv7q//vWvxMXFMXv2bIqKigDYunUrGzdu5NZbb6Vt27YcO3aMN954g+HDh7N3717rjFhhYSGXXXYZ+/bt4+677+aiiy4iJyeHb7/9lpMnT9K3b1/GjRvHZ599xosvvlhjtuWTTz5BURQmTJjg0LiFa8l7srwnt5T35IaUlJQwfPhwDh8+zIwZM0hJSeGLL75g0qRJnD9/3vqH9OrVq7ntttu46qqr+Ne//gWoa/s3bNhgPefpp59m/vz5TJkyhUGDBpGfn8+2bdvYsWMHV199tVPjdDmlmZk+fbpy4csaNmyYAigLFy6sdX5xcXGtY3/5y1+U4OBgpbS01HrsrrvuUtq3b2/9Oi0tTQGUmJgY5ezZs9bj33zzjQIo3333nfXYnDlzao0JUAICApTDhw9bj+3evVsBlFdffdV6bMyYMUpwcLBy6tQp67FDhw4pfn5+ta5Zl7pe3/z58xWdTqccP368xusDlLlz59Y4t1+/fkr//v2tXy9dulQBlP/3//6f9VhlZaVy2WWXKYDy3nvvNTqmgQMHKm3btlVMJpP12IoVKxRAefPNN63XLCsrq/G8c+fOKfHx8crdd99d4zigzJkzx/r1e++9pwBKWlqaoiiKkp2drQQEBCjXXXedYjabref94x//UADlrrvush4rLS2tMS5FUf9bG43GGj+brVu31vt6L/xd0X5mzz33XI3z/vznPys6na7G74Ctvxf1KS8vV2JiYpQnnnjCeuz2229X+vTpU+O8//3vfwqgPPDAA7Wuof2MDh06pOj1emXcuHG1fibVf44X/vw17du3r/Gz1f67XHrppUplZWWNc+v6Pd20aZMCKB988IH12OzZsxVAWbJkSb3jXrlypQIoP/zwQ43v9+7dWxk2bFit5wn3kvfkxl+fvCermtt7svY7+fzzz9d7zssvv6wAykcffWQ9Vl5ergwZMkQJDQ1V8vPzFUVRlAcffFAJDw+v9d5ZXZ8+fZTrrruuwTH5ihaRdgcwGo1Mnjy51vGgoCDr44KCAnJycrjssssoLi5m//79jV53/PjxREVFWb/W/uI6evRoo88dMWIEqamp1q979+5NeHi49bkmk4k1a9YwduxYWrdubT2vY8eOjBo1qtHrQ83XV1RURE5ODkOHDkVRFHbu3Fnr/Pvuu6/G15dddlmN17J8+XL8/Pysf3WDup7n/vvvt2k8oK4JO3nyJD///LP12OLFiwkICODmm2+2XjMgIABQ08Nnz56lsrKSAQMG1JkeasiaNWsoLy/n/vvvr5EWe+ihh2qdazQa0evV/y1MJhO5ubmEhobSpUsXu++rWb58OQaDgQceeKDG8b/97W8oisIPP/xQ43hjvxcN+eGHH8jNzeW2226zHrvtttvYvXt3jZTWV199hU6nY86cObWuof2Mli5ditlsZvbs2dafyYXnOGLq1Km11n9V/z2tqKggNzeXjh07EhkZWePn/tVXX9GnTx/GjRtX77hHjBhB69at+fjjj63f+/333/ntt98aXXcoPEfek+U9uSW8J9syloSEhBrv2f7+/jzwwAMUFhby008/ARAZGUlRUVGDKfTIyEj++OMPDh065PS43K3FBJ9t2rSx/o9T3R9//MG4ceOIiIggPDycuLg46z9QeXl5jV63Xbt2Nb7W3vTOnTtn93O152vPzc7OpqSkhI4dO9Y6r65jdUlPT2fSpElER0db1wwNGzYMqP36tHV/9Y0H1LV5iYmJhIaG1jivS5cuNo0H4NZbb8VgMLB48WIASktL+frrrxk1alSNfzTef/99evfubV27EhcXx7Jly2z671Ld8ePHAejUqVON43FxcTXuB+qb6ksvvUSnTp0wGo3ExsYSFxfHb7/9Zvd9q9+/devWhIWF1TiuVftq49M09nvRkI8++oiUlBSMRiOHDx/m8OHDpKamEhwcXCMYO3LkCK1btyY6Orreax05cgS9Xk/37t0bva89UlJSah0rKSlh9uzZ1vVX2s/9/PnzNX7uR44coWfPng1eX6/XM2HCBJYuXUpxcTGgLkUIDAy0/kMqvE/ek+U9uSW8J9sylk6dOtX6A//Csfz1r3+lc+fOjBo1irZt23L33XfXWnc6d+5czp8/T+fOnenVqxd///vffbZFVosJPqv/tak5f/48w4YNY/fu3cydO5fvvvuO1atXW9dT2NKaob4KPuWCRcuufq4tTCYTV199NcuWLeOxxx5j6dKlrF692roI+8LX56lqxFatWnH11Vfz1VdfUVFRwXfffUdBQUGNtXgfffQRkyZNIjU1lXfeeYcVK1awevVqrrzySre2zJg3bx4zZ87k8ssv56OPPmLlypWsXr2aHj16eKxVh6O/F/n5+Xz33XekpaXRqVMn60f37t0pLi5m8eLFLvvdssWFRRGauv5fvP/++/nnP//JLbfcwueff86qVatYvXo1MTExDv3cJ06cSGFhIUuXLrVW/19//fVERETYfS3hHvKeLO/JtmjK78mu1KpVK3bt2sW3335rXa86atSoGmt7L7/8co4cOcK7775Lz549efvtt7nooot4++23PTZOW7WYgqO6rFu3jtzcXJYsWcLll19uPZ6WlubFUVVp1aoVgYGBdTYAbqgpsGbPnj0cPHiQ999/n4kTJ1qPO1P51r59e9auXUthYWGNv7QPHDhg13UmTJjAihUr+OGHH1i8eDHh4eGMGTPG+v0vv/ySDh06sGTJkhppmbrSxLaMGeDQoUN06NDBevzMmTO1/nL98ssvueKKK3jnnXdqHD9//jyxsbHWr+1JO7dv3541a9ZQUFBQ4y9tLYWojc9ZS5YsobS0lDfeeKPGWEH97/Pkk0+yYcMGLr30UlJTU1m5ciVnz56td/YzNTUVs9nM3r17GywmiIqKqlVZW15eTkZGhs1j//LLL7nrrrtYsGCB9VhpaWmt66ampvL77783er2ePXvSr18/Pv74Y9q2bUt6ejqvvvqqzeMR3iHvyfaT92SVL74n2zqW3377DbPZXGP2s66xBAQEMGbMGMaMGYPZbOavf/0rb775Jk899ZR15j06OprJkyczefJkCgsLufzyy3n66ad9rt1ei5n5rIv210z1v17Ky8t5/fXXvTWkGgwGAyNGjGDp0qWcPn3aevzw4cO11qTU93yo+foURanRmsFeo0ePprKykjfeeMN6zGQy2f0P+9ixYwkODub111/nhx9+4MYbbyQwMLDBsf/6669s2rTJ7jGPGDECf39/Xn311RrXe/nll2udazAYav01+8UXX3Dq1Kkax7TelLa0Mxk9ejQmk4n//Oc/NY6/9NJL6HQ6m9eKNeajjz6iQ4cO3Hffffz5z3+u8fHII48QGhpqTb3fdNNNKIrCM888U+s62usfO3Yser2euXPn1pphqP4zSk1NrbFWDOC///1vvTOfdanr5/7qq6/WusZNN93E7t27+frrr+sdt+bOO+9k1apVvPzyy8TExLjs5yzcR96T7SfvySpffE+2xejRo8nMzOSzzz6zHqusrOTVV18lNDTUuiQjNze3xvP0er218X9ZWVmd54SGhtKxY0fr931Ji575HDp0KFFRUdx1113WbcY+/PBDj06lN+bpp59m1apVXHLJJUybNs36P0zPnj0b3Uasa9eupKam8sgjj3Dq1CnCw8P56quvnFqnMmbMGC655BIef/xxjh07Rvfu3VmyZInda29CQ0MZO3asdY3Rhe1vrr/+epYsWcK4ceO47rrrSEtLY+HChXTv3p3CwkK77qX1xps/fz7XX389o0ePZufOnfzwww+1Zgivv/565s6dy+TJkxk6dCh79uzh448/rvHXOagBV2RkJAsXLiQsLIyQkBAGDx5c53rGMWPGcMUVV/DEE09w7Ngx+vTpw6pVq/jmm2946KGHaixkd9Tp06f58ccfay2g1xiNRkaOHMkXX3zBK6+8whVXXMGdd97JK6+8wqFDh7j22msxm8388ssvXHHFFcyYMYOOHTvyxBNP8Oyzz3LZZZdx4403YjQa2bp1K61bt7b2y5wyZQr33XcfN910E1dffTW7d+9m5cqVtX62Dbn++uv58MMPiYiIoHv37mzatIk1a9bUamPy97//nS+//JKbb76Zu+++m/79+3P27Fm+/fZbFi5cSJ8+fazn3n777Tz66KN8/fXXTJs2TRpNNwHynmw/eU9W+dp7cnVr166ltLS01vGxY8dy77338uabbzJp0iS2b99OcnIyX375JRs2bODll1+2zsxOmTKFs2fPcuWVV9K2bVuOHz/Oq6++St++fa3rQ7t3787w4cPp378/0dHRbNu2jS+//JIZM2a49PW4hAcq6j2qvrYePXr0qPP8DRs2KBdffLESFBSktG7dWnn00UetrVp+/PFH63n1tfWoq4UCF7SZqK+tx/Tp02s998L2NIqiKGvXrlX69eunBAQEKKmpqcrbb7+t/O1vf1MCAwPr+SlU2bt3rzJixAglNDRUiY2NVaZOnWptE1G9JcVdd92lhISE1Hp+XWPPzc1V7rzzTiU8PFyJiIhQ7rzzTmXnzp02t/XQLFu2TAGUxMTEOlv5zJs3T2nfvr1iNBqVfv36Kd9//32t/w6K0nhbD0VRFJPJpDzzzDNKYmKiEhQUpAwfPlz5/fffa/28S0tLlb/97W/W8y655BJl06ZNyrBhw2q16fnmm2+U7t27W1usaK+9rjEWFBQoDz/8sNK6dWvF399f6dSpk/L888/XaDOivRZbfy+qW7BggQIoa9eurfecRYsWKYDyzTffKIqitk55/vnnla5duyoBAQFKXFycMmrUKGX79u01nvfuu+8q/fr1U4xGoxIVFaUMGzZMWb16tfX7JpNJeeyxx5TY2FglODhYGTlypHL48OF6Wy1t3bq11tjOnTunTJ48WYmNjVVCQ0OVkSNHKvv376/zdefm5iozZsxQ2rRpowQEBCht27ZV7rrrLiUnJ6fWdUePHq0AysaNG+v9uQj3kvfkmuQ9WdXc35MVpep3sr6PDz/8UFEURcnKyrK+/wUEBCi9evWq9d/tyy+/VK655hqlVatWSkBAgNKuXTvlL3/5i5KRkWE957nnnlMGDRqkREZGKkFBQUrXrl2Vf/7zn0p5eXmD4/QGnaL40J+UwmZjx45tMi0VhPCWcePGsWfPHpvW4wnhDHlPFsJ2LXrNZ1Nx4bZrhw4dYvny5QwfPtw7AxKiCcjIyGDZsmXceeed3h6KaGbkPVkI58jMZxOQmJjIpEmT6NChA8ePH+eNN96grKyMnTt31uqTJkRLl5aWxoYNG3j77bfZunUrR44cISEhwdvDEs2IvCcL4ZwWXXDUVFx77bV88sknZGZmYjQaGTJkCPPmzZM3OSHq8NNPPzF58mTatWvH+++/L4GncDl5TxbCOTLzKYQQQgghPEbWfAohhBBCCI+R4FMIIYQQQnhMk1jzaTabOX36NGFhYXZtoSWEELZSFIWCggJat25dY5u75kLeR4UQ7mbr+2iTCD5Pnz5NUlKSt4chhGgBTpw4Qdu2bb09DJeT91EhhKc09j7aJIJPbXupEydOEB4e7uXRCCGao/z8fJKSkqzvN82NvI8KIdzN1vfRJhF8aimi8PBwedMUQrhVc01Jy/uoEMJTGnsfbX4Lm4QQQgghhM+S4FMIIYQQQniMBJ9CCCGEEMJjmsSaTyGEEELYzmQyUVFR4e1hiGbG398fg8Hg9HUk+BRCCCGaCUVRyMzM5Pz5894eimimIiMjSUhIcKo4U4JPIYQQopnQAs9WrVoRHBzcbLs3CM9TFIXi4mKys7MBSExMdPhaEnwKIYQQzYDJZLIGnjExMd4ejmiGgoKCAMjOzqZVq1YOp+Cl4EgIIYRoBrQ1nsHBwV4eiWjOtN8vZ9YUS/AphBBCNCOSahfu5IrfLwk+hRBCCCGEx0jwKYQQQohmJzk5mZdfftnm89etW4dOp5NOAR4gwacQQgghvEan0zX48fTTTzt03a1bt3LvvffafP7QoUPJyMggIiLCofvZSoJcqXYXQgghhBdlZGRYH3/22WfMnj2bAwcOWI+FhoZaHyuKgslkws+v8fAlLi7OrnEEBASQkJBg13OEY2TmUwghhBBek5CQYP2IiIhAp9NZv96/fz9hYWH88MMP9O/fH6PRyPr16zly5Ag33HAD8fHxhIaGMnDgQNasWVPjuhem3XU6HW+//Tbjxo0jODiYTp068e2331q/f+GM5KJFi4iMjGTlypV069aN0NBQrr322hrBcmVlJQ888ACRkZHExMTw2GOPcddddzF27FiHfx7nzp1j4sSJREVFERwczKhRozh06JD1+8ePH2fMmDFERUUREhJCjx49WL58ufW5EyZMIC4ujqCgIDp16sR7773n8FjcRYJPIYQQoplSFIXi8kqvfCiK4rLX8fjjj/N///d/7Nu3j969e1NYWMjo0aNZu3YtO3fu5Nprr2XMmDGkp6c3eJ1nnnmGW265hd9++43Ro0czYcIEzp49W+/5xcXFvPDCC3z44Yf8/PPPpKen88gjj1i//69//YuPP/6Y9957jw0bNpCfn8/SpUudeq2TJk1i27ZtfPvtt2zatAlFURg9erS1tdH06dMpKyvj559/Zs+ePfzrX/+yzg4/9dRT7N27lx9++IF9+/bxxhtvEBsb69R43EHS7kIIIUQzVVJhovvslV659965IwkOcE2YMXfuXK6++mrr19HR0fTp08f69bPPPsvXX3/Nt99+y4wZM+q9zqRJk7jtttsAmDdvHq+88gpbtmzh2muvrfP8iooKFi5cSGpqKgAzZsxg7ty51u+/+uqrzJo1i3HjxgHwn//8xzoL6YhDhw7x7bffsmHDBoYOHQrAxx9/TFJSEkuXLuXmm28mPT2dm266iV69egHQoUMH6/PT09Pp168fAwYMANTZX18kM59CCCGE8GlaMKUpLCzkkUceoVu3bkRGRhIaGsq+ffsanfns3bu39XFISAjh4eHW7SLrEhwcbA08Qd1SUjs/Ly+PrKwsBg0aZP2+wWCgf//+dr226vbt24efnx+DBw+2HouJiaFLly7s27cPgAceeIDnnnuOSy65hDlz5vDbb79Zz502bRqffvopffv25dFHH2Xjxo0Oj8WdZOZTCCGEaKaC/A3snTvSa/d2lZCQkBpfP/LII6xevZoXXniBjh07EhQUxJ///GfKy8sbvI6/v3+Nr3U6HWaz2a7zXbmcwBFTpkxh5MiRLFu2jFWrVjF//nwWLFjA/fffz6hRozh+/DjLly9n9erVXHXVVUyfPp0XXnjBq2O+kMx8CiGEEM2UTqcjOMDPKx/u3Glpw4YNTJo0iXHjxtGrVy8SEhI4duyY2+5Xl4iICOLj49m6dav1mMlkYseOHQ5fs1u3blRWVvLrr79aj+Xm5nLgwAG6d+9uPZaUlMR9993HkiVL+Nvf/sZbb71l/V5cXBx33XUXH330ES+//DL//e9/HR6Pu8jMpxBCCCGalE6dOrFkyRLGjBmDTqfjqaeeanAG013uv/9+5s+fT8eOHenatSuvvvoq586dsynw3rNnD2FhYdavdTodffr04YYbbmDq1Km8+eabhIWF8fjjj9OmTRtuuOEGAB566CFGjRpF586dOXfuHD/++CPdunUDYPbs2fTv358ePXpQVlbG999/b/2eL5HgUwghhBBNyosvvsjdd9/N0KFDiY2N5bHHHiM/P9/j43jsscfIzMxk4sSJGAwG7r33XkaOHInB0PiSg8svv7zG1waDgcrKSt577z0efPBBrr/+esrLy7n88stZvny5dQmAyWRi+vTpnDx5kvDwcK699lpeeuklQO1VOmvWLI4dO0ZQUBCXXXYZn376qetfuJN0ip2LF37++Weef/55tm/fTkZGBl9//XWj/azWrVvHzJkz+eOPP0hKSuLJJ59k0qRJNt8zPz+fiIgI8vLyCA8Pt2e4Qghhk+b+PtPcX5+A0tJS0tLSSElJITAw0NvDaZHMZjPdunXjlltu4dlnn/X2cNyiod8zW99n7F7zWVRURJ8+fXjttddsOj8tLY3rrruOK664gl27dvHQQw8xZcoUVq70TusHIYQQQghXOH78OG+99RYHDx5kz549TJs2jbS0NG6//XZvD82n2Z12HzVqFKNGjbL5/IULF5KSksKCBQsAdTHt+vXreemllxg50jsVeEIIIYQQztLr9SxatIhHHnkERVHo2bMna9as8cl1lr7E7Ws+N23a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8nKXDXfTpk1MmDCBZ555hpEjRxIREcGnn37KggULXHaP6rSUt0an02E2m91yL1Ar9W+//XaWLVvGDz/8wJw5c/j0008ZN24cU6ZMYeTIkSxbtoxVq1Yxf/58FixYwP333++WsUjBkRD1+PfaQ5w6X0KbyCAevrqze25SXyFPmP1FR25xbD2U5UFIHLQd6LrrJvSGiCSoLKlaTyp8lqTemzCdTk19e+PDzkzJLbfcgl6vZ/HixXzwwQfcfffd1iVEGzZs4IYbbuCOO+6gT58+dOjQgYMHD9p87W7dunHixAkyMqreUzdv3lzjnI0bN9K+fXueeOIJBgwYQKdOnTh+/HiNcwICAjCZTI3ea/fu3RQVFVmPbdiwAb1eT5cuXWwesz2013fiRFULu71793L+/Hm6d6+awOjcuTMPP/wwq1at4sYbb+S9996zfi8pKYn77ruPJUuW8Le//Y233nrLLWMFCT6FqNO+jHze/iUNgLk39CDEHanG0jxI+1l93HVMze+FO95uyaW04LjLaNC7qIAJ1H+UrHu9y25Hvq5bYhgge7wL9woNDWX8+PHMmjWLjIyMGhvSdOrUidWrV7Nx40b27dvHX/7ylxqV3I0ZMWIEnTt35q677mL37t388ssvPPHEEzXO6dSpE+np6Xz66accOXKEV155ha+//rrGOcnJydZtxXNycigrK6t1rwkTJhAYGMhdd93F77//zo8//sj999/PnXfeaU25O8pkMlm3ONc+9u3bx4gRI+jVqxcTJkxgx44dbNmyhYkTJzJs2DAGDBhASUkJM2bMYN26dRw/fpwNGzawdetWunXrBsBDDz3EypUrSUtLY8eOHfz444/W77mDBJ9CXMBkVpi1ZA8ms8Konglc1c25N4t6HVoN5gqI7QKxHWt+T5v59GbwaTa7Zlej+mjB54HlYKp0/fWFy3RPVCt692YUeHkkorm75557OHfuHCNHjqyxPvPJJ5/koosuYuTIkQwfPpyEhATGjh1r83X1ej1ff/01JSUlDBo0iClTpvDPf/6zxjl/+tOfePjhh5kxYwZ9+/Zl48aNPPXUUzXOuemmm7j22mu54ooriIuLq7PdU3BwMCtXruTs2bMMHDiQP//5z1x11VX85z//se+HUYfCwkLrFufax5gxY9DpdHzzzTdERUVx+eWXM2LECDp06MBnn30GgMFgIDc3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frq9vow3vt+pPeIdzHWTT5VacmlHjhyxPyZPnkxwcHCpY6NGjbKfaxgGBQUFZWq3Zs2a5Vp45e3tXal1I3/55RfOnDlD3759+eCDDyrlmpeihTsi4kqaRwUxc0hHPnvkWq6pH8qZ/EKm/rCHbq8vY/aKfeQWFDo7RJfgusmnrci8l5JPVxQVFWV/hISEYLFY7L//9ttvBAUF8d133xEXF4ePjw+//PILe/fu5a677iIyMpLAwEA6duzIkiVLSrV77rC7xWLh/fff5+6778bf35+YmBi++eYb++vnDrvPmTOH0NBQFi1aRMuWLQkMDKRXr14cOXLE/p6CggKefPJJQkNDqVGjBqNHj2bw4MH06dPnsp975syZ3H///TzwwAPMmjXrvNcPHjzIgAEDCA8PJyAggPj4eNasWWN//dtvv6Vjx474+voSERHB3XffXeqzfv3116XaCw0NZc6cOQAkJydjsVj47LPP6NatG76+vnzyySecOHGCAQMGULduXfz9/Wnbti2ffvppqXaKiop47bXXaNq0KT4+PtSvX59XXnkFgB49ejBixIhS5x87dgxvb2+WLl162e9ERMTROjeuwZePXsf0QXE0rhnAyaw8Xvz2VxLe/In/Jh2iSPvEXxUXTj7V83mlDMMgO6/AKQ/DcNy/0M8++ywTJ05kx44dtGvXjszMTG677TaWLl3Kpk2b6NWrF71792b//v2XbOfFF1/kvvvuY8uWLdx2220MHDiQkydPXvT87OxsJk2axEcffcTPP//M/v37S/XEvvrqq3zyySfMnj2bFStWkJ6efl7SdyEZGRnMnz+fQYMGcfPNN5OWlsby5cvtr2dmZtKtWzcOHTrEN998w+bNm3nmmWcoKioCYMGCBdx9993cdtttbNq0iaVLl9KpU6fLXvdczz77LE899RQ7duwgMTGRnJwc4uLiWLBgAdu2beORRx7hgQceYO3atfb3jBkzhokTJzJ27Fh+/fVX5s6dS2RkJAAPP/wwc+fOJTc3137+xx9/TN26denRo0e54xMRcQSLxUKvNlF8//SN/OvuttQK8uHAyTM8NS+J3m//wvLdx5wdYrXl+kXmvbXavbzO5BfS6oVFTrn2ry8l4u/tmD/Ll156iZtvvtn+e3h4OLGxsfbfX375Zb766iu++eab83rezjZkyBAGDBgAwL/+9S+mTJnC2rVr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H2TOnDk899xz9tV48+fPp7CwkAEDBpCZmUlcXByjR48mODiYBQsW8MADD9CkSZNL1lO0KSoq4p577iEyMpI1a9aQlpZWan6oTVBQEHPmzKFOnTps3bqV4cOHExQUxDPPPEO/fv3Ytm0bCxcutCdWISEh57WRlZVFYmIiXbp0Yd26dRw9epSHH36YESNGlEqwf/zxR2rXrs2PP/7Inj176NevH+3bt2f48OEX/Rx79+5l1apVfPnllxiGwV//+lf++OMPGjQwF+QdOnSIG2+8ke7du/PDDz8QHBzMihUr7L2T7777LiNHjmTixInceuutpKWlXdH2oM8++yyTJk2icePGhIWFceDAAW677TZeeeUVfHx8+PDDD+nduzc7d+6kfv36gLld76pVq5gyZQqxsbHs27eP48ePY7FYeOihh5g9ezajRo2yX2P27NnceOONNG3atNzxVabyblP81FNP0a1bN9544w1uv/125s2bx/r163nvvfec+TFERK6MUQ2kpaUZgJGWlubsUFzSmTNnjF9//dU4c+aMeSA30zDGBTvnkZtZ5rh37NhhAMaPP/5oP9a1a1dj0KBBF33P7bffbvztb3+z/96tWzfjqaeesv/eoEED49///rdhGIaxaNEiw9PT0zh06JD99e+++84AjK+++uqi13j99deNuLg4++/jxo0zYmNjzzvv7Hbee+89IywszMjMLPn8CxYsMKxWq5GSkmIYhmEMHjzYaNCggVFQUGA/59577zX69et30VgMwzD+8Y9/GH369LH/ftdddxnjxo2z/z5mzBijUaNGRl5e3gXfX6dOHeO555674Gv79u0zAGPTpk32Y6dOnSr1z+XHH380AOPrr7++ZJyGYRitW7c2pk6dahiGYezcudMAjMWLF1/w3EOHDhkeHh7GmjVrDMMwjLy8PCMiIsKYM2fORds/72/9LJV9n5k6dapRv359w9vb2+jUqZOxevVq+2vdunUzBg8eXOr8zz//3GjWrJnh7e1ttG7d2liwYEG5rqf7qIhUtLLeZzTsLtVWixYtuO6665g1axYAe/bsYfny5QwbNgyAwsJCXn75Zdq2bUt4eDiBgYEsWrSI/fv3l6n9HTt2EB0dTZ06dezHLjTM+dlnn3H99dcTFRVFYGAgzz//fJmvcfa1YmNjCQgoqU17/fXXU1RUxM6dO+3HWrdujYdHyVZptWvX5ujRoxdtt7CwkA8++IBBgwbZjw0aNIg5c+ZQVGSW0EhKSqJr1654eXmd9/6jR49y+PBhevbsWa7PcyHx8fGlfs/MzGTUqFG0bNmS0NBQAgMD2bFjh/27S0pKwsPDg27dul2wvTp16nD77bfb//l/++235Obmcu+99151rJVhxIgR/PHHH+Tm5rJmzRo6d+5sf23ZsmXnTSm599572blzJ7m5uWzbtk27G4lItaVhdzmflz/847Dzrl0Ow4YN44knnmDatGnMnj2bJk2a2JOV119/nbfeeovJkyfTtm1bAgICePrpp8nLy3NYuKtWrWLgwIG8+OKLJCYmEhISwrx583jjjTccdo2znZsgWiwWexJ5IYsWLeLQoUP069ev1PHCwkKWLl3KzTffjJ+f30Xff6nXwKxPCeYiIpuLzUE9O7EGGDVqFIsXL2bSpEk0bdoUPz8/+vbta//nc7lrAzz88MM88MAD/Pvf/2b27Nn069ev0haMiYjIlVHPp5zPYjF3h3LGo5w7Kdx3331YrVbmzp3Lhx9+yEMPPWSf/7lixQruuusuBg0aRGxsLI0bN2bXrl1lbrtly5YcOHCAI0eO2I+tXr261DkrV66kQYMGPPfcc8THxxMTE8Mff/xR6hxvb28KCwsve63NmzeTlZVlP7ZixQqsVivNmzcvc8znmjlzJv379ycpKanUo3///vaFR+3atWP58uUXTBqDgoJo2LDheYtdbGrWrAlQ6js6e/HRpaxYsYIhQ4Zw991307ZtW6KiokhOTra/3rZtW4qKivjpp58u2sZtt91GQEAA7777LgsXLuShhx4q07VFRMR5lHxKtRYYGEi/fv0YM2YMR44cYciQIfbXYmJiWLx4MStXrmTHjh38+c9/Pq9czaUkJCTQrFkzBg8ezObNm1m+fDnPPfdcqXNiYmLYv38/8+bNY+/evUyZMoWvvvqq1DkNGzZk3759JCUlcfz48QvW2Rw4cCC+vr4MHjyYbdu28eOPP/LEE0/wwAMPnFdcvKyOHTvGt99+y+DBg2nTpk2px4MPPsjXX3/NyZMnGTFiBOnp6fTv35/169eze/duPvroI/tw//jx43njjTeYMmUKu3fvZuPGjUydOhUweyevvfZaJk6cyI4dO/jpp594/vnnyxRfTEwMX375JUlJSWzevJn777+/VC9uw4YNGTx4MA899BBff/01+/btY9myZXz++ef2czw8PBgyZAhjxowhJiZGq79FRKoBJZ9S7Q0bNoxTp06RmJhYan7m888/T4cOHUhMTKR79+5ERUXRp0+fMrdrtVr56quvOHPmDJ06deLhhx/mlVdeKXXOnXfeyV//+ldGjBhB+/btWblyJWPHji11zp/+9Cd69erFTTfdRM2aNS9Y7snf359FixZx8uRJOnbsSN++fenZsydvv/12+b6Ms3z44YcEBARccL5mz5498fPz4+OPP6ZGjRr88MMPZGZm0q1bN+Li4pgxY4Z9iH/w4MFMnjyZd955h9atW3PHHXewe/due1uzZs2ioKCAuLg4nn76af75z3+WKb4333yTsLAwrrvuOnr37k1iYiIdOnQodc67775L3759eeyxx2jRogXDhw8v1TsM5j//vLw8+0pxERGp2izG2ZO1qqj09HRCQkJIS0tToeQKkJOTw759+2jUqBG+vr7ODkekXJYvX07Pnj05cODAZXuJL/W37ur3GVf/fCLifGW9z2jBkYhUS7m5uRw7dozx48dz7733XvH0BBERqVwadheRaunTTz+lQYMGnD59mtdee83Z4YiISBkp+RSRamnIkCEUFhayYcMG6tat6+xwRESkjJR8ioiIiEilUfIpIiIiIpVGyafYXWqnHBFXoL9xERHn02p3wdvbG6vVyuHDh6lZsybe3t72XYJEXIFhGOTl5XHs2DGsVive3t7ODklExG0p+RSsViuNGjXiyJEjHD7spD3dRSqBv78/9evXt+9JLyIilU/JpwBm72f9+vUpKCi47D7kItWRh4cHnp6e6tUXEXEyJZ9iZ7FY8PLysm+rKCIiIuJoGnsSERERkUqj5FNEREREKo2STxERERGpNNVizqdhGACkp6c7ORIRcVW2+4vtfuNqdB8VkYpW1vtotUg+MzIyAIiOjnZyJCLi6jIyMggJCXF2GA6n+6iIVJbL3UctRjX43/yioiIOHz5MUFBQmcukpKenEx0dzYEDBwgODq7gCKs2fRcl9F2Upu+jhGEYZGRkUKdOHZesA6r76NXRd1Gavo8S+i5KlPU+Wi16Pq1WK/Xq1bui9wYHB7v9H4ONvosS+i5K0/dhcsUeTxvdRx1D30Vp+j5K6LswleU+6nr/ey8iIiIiVZaSTxERERGpNC6bfPr4+DBu3Dh8fHycHYrT6bsooe+iNH0fcin6+yih76I0fR8l9F2UX7VYcCQiIiIirsFlez5FREREpOpR8ikiIiIilUbJp4iIiIhUGiWfIiIiIlJpXDL5nDZtGg0bNsTX15fOnTuzdu1aZ4fkFOPHj8disZR6tGjRwtlhVYqff/6Z3r17U6dOHSwWC19//XWp1w3D4IUXXqB27dr4+fmRkJDA7t27nRNsJbjc9zFkyJDz/lZ69erlnGClStB91KT7qO6jNrqPOo7LJZ+fffYZI0eOZNy4cWzcuJHY2FgSExM5evSos0NzitatW3PkyBH745dffnF2SJUiKyuL2NhYpk2bdsHXX3vtNaZMmcL06dNZs2YNAQEBJCYmkpOTU8mRVo7LfR8AvXr1KvW38umnn1ZihFKV6D5amu6juo+C7qMOZbiYTp06GY8//rj998LCQqNOnTrGhAkTnBiVc4wbN86IjY11dhhOBxhfffWV/feioiIjKirKeP311+3HTp8+bfj4+BiffvqpEyKsXOd+H4ZhGIMHDzbuuusup8QjVY/uoyV0HzXpPlqa7qNXx6V6PvPy8tiwYQMJCQn2Y1arlYSEBFatWuXEyJxn9+7d1KlTh8aNGzNw4ED279/v7JCcbt++faSkpJT6OwkJCaFz585u+3cCsGzZMmrVqkXz5s159NFHOXHihLNDEifQffR8uo+eT/fRC9N9tGxcKvk8fvw4hYWFREZGljoeGRlJSkqKk6Jyns6dOzNnzhwWLlzIu+++y759++jatSsZGRnODs2pbH8L+jsp0atXLz788EOWLl3Kq6++yk8//cStt95KYWGhs0OTSqb7aGm6j16Y7qPn03207DydHYBUnFtvvdX+vF27dnTu3JkGDRrw+eefM2zYMCdGJlVN//797c/btm1Lu3btaNKkCcuWLaNnz55OjEzEuXQflbLSfbTsXKrnMyIiAg8PD1JTU0sdT01NJSoqyklRVR2hoaE0a9aMPXv2ODsUp7L9Lejv5OIaN25MRESE2/+tuCPdRy9N91GT7qOXp/voxblU8unt7U1cXBxLly61HysqKmLp0qV06dLFiZFVDZmZmezdu5fatWs7OxSnatSoEVFRUaX+TtLT01mzZo3+ToodPHiQEydOuP3fijvSffTSdB816T56ebqPXpzLDbuPHDmSwYMHEx8fT6dOnZg8eTJZWVkMHTrU2aFVulGjRtG7d28aNGjA4cOHGTduHB4eHgwYMMDZoVW4zMzMUv+3uW/fPpKSkggPD6d+/fo8/fTT/POf/yQmJoZGjRoxduxY6tSpQ58+fZwXdAW61PcRHh7Oiy++yJ/+9CeioqLYu3cvzzzzDE2bNiUxMdGJUYuz6D5aQvdR3UdtdB91IGcvt68IU6dONerXr294e3sbnTp1MlavXu3skJyiX79+Ru3atQ1vb2+jbt26Rr9+/Yw9e/Y4O6xK8eOPPxrAeY/BgwcbhmGWCRk7dqwRGRlp+Pj4GD179jR27tzp3KAr0KW+j+zsbOOWW24xatasaXh5eRkNGjQwhg8fbqSkpDg7bHEi3UdNuo/qPmqj+6jjWAzDMCo33RURERERd+VScz5FREREpGpT8ikiIiIilUbJp4iIiIhUGiWfIiIiIlJplHyKiIiISKVR8ikiIiIilUbJp4iIiIhUGiWfIiIiIlJplHyKiIiISKVR8ikiIiIilUbJp4iIiIhUGiWfIiIiIlJp/j9/wi7NfpKEbAAAAABJRU5ErkJggg==\n"
          },
          "metadata": {}
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from sklearn.metrics import classification_report\n",
        "def evaluate_model(val_ds, model):\n",
        "    y_pred = []\n",
        "    y_true = []\n",
        "\n",
        "    for batch_images, batch_labels in val_ds:\n",
        "        predictions = model.predict(batch_images, verbose=0)\n",
        "        y_pred = y_pred + np.argmax(tf.nn.softmax(predictions), axis=1).tolist()\n",
        "        y_true = y_true + batch_labels.numpy().tolist()\n",
        "    print(classification_report(y_true, y_pred))\n",
        "\n",
        "evaluate_model(val_ds, model)"
      ],
      "metadata": {
        "id": "O-CbkVC4lHjc",
        "outputId": "52443b1a-eed8-444f-a524-2b250e8727f3",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "execution_count": 17,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "              precision    recall  f1-score   support\n",
            "\n",
            "           0       0.75      1.00      0.86         3\n",
            "           1       1.00      1.00      1.00         6\n",
            "           2       1.00      0.86      0.92         7\n",
            "\n",
            "    accuracy                           0.94        16\n",
            "   macro avg       0.92      0.95      0.93        16\n",
            "weighted avg       0.95      0.94      0.94        16\n",
            "\n"
          ]
        }
      ]
    }
  ]
}