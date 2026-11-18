# Flentio Platform: Enterprise System Requirements

Para desplegar la plataforma Flentio de forma autónoma con orquestación total de RAG (Retrieval-Augmented Generation) sobre contenedores TEI (Text Embeddings Inference) locales, el servidor físico o máquina virtual debe cumplir estrictamente con los siguientes requisitos:

## 1. Hardware Mínimo Recomendado

| Componente | Requisito Mínimo | Configuración Recomendada (Producción) |
| :--- | :--- | :--- |
| **CPU** | 8 Cores (x86_64) | 16+ Cores |
| **Memoria RAM** | 16 GB DDR4 | 32 GB DDR4 o superior |
| **Almacenamiento** | 100 GB (SSD/NVMe) | 500 GB NVMe (Para escalabilidad PostgreSQL y MinIO) |
| **Red** | 1 Gbps | 10 Gbps |

## 2. Requisitos de Aceleración (GPU)

El motor Semántico y de Reranking de Flentio (Dual-TEI) depende fundamentalmente del cómputo en la capa de inferencia nativa. Por ende, **se requiere hardware NVIDIA** compatible con el ecosistema CUDA:

*   **Arquitectura mínima:** NVIDIA Ampere (Compute Capability 8.6+). Ej. RTX 3060, A10g.
*   **Arquitectura recomendada:** NVIDIA Ada Lovelace / Hopper (Ej. L4, A100, H100).
*   **VRAM mínima:** 8 GB VRAM.
*   **VRAM recomendada:** 16 GB+ VRAM.

> [!WARNING]
> Ejecutar TEI en servidores sin GPU NVIDIA obligará a emular modelos de incrustación de manera no optimizada, lo cual incrementará exponencialmente la latencia RAG por cada solicitud (>30 segundos).

## 3. Requisitos de Software

*   **Sistema Operativo:** Ubuntu 22.04 LTS (o superior) / RHEL 9. En entornos Windows, se requiere Windows 11 Pro/Enterprise con **WSL2**.
*   **Motor de Contenedores:** Docker Engine v24.0+ y Docker Compose v2.20+.
*   **NVIDIA Container Toolkit:** Indispensable para exponer la GPU local a las imágenes `ghcr.io/huggingface/text-embeddings-inference`.

## 4. Puertos Requeridos (Exposición Interna/Externa)

El entorno `docker-compose` de despliegue requiere que los siguientes puertos estén disponibles en el host:

| Puerto | Protocolo | Servicio | Visibilidad Recomendada |
| :--- | :--- | :--- | :--- |
| **3000** | TCP | Interfaz Web / Dashboard Flentio | Proxy Inverso (HTTPS) Externa |
| **5432** | TCP | PostgreSQL (Flentio_RAG) | Localhost / Red Interna |
| **8085** | TCP | TEI (Reranker) | Localhost / Aislada |
| **8086** | TCP | TEI (Embeddings) | Localhost / Aislada |
| **9000/9001** | TCP | MinIO (Object Storage & Console) | Localhost / Red Interna |
| **3310** | TCP | ClamAV (Malware Scanner) | Aislada |

## 5. Instrucciones de Despliegue Zero-Touch

El paquete de entrega de Flentio ha sido adaptado para no requerir intervención manual compleja:

1. Descomprime el archivo `.tar.gz` o `.zip` en el servidor destino.
2. Otorga permisos de ejecución a los scripts: `chmod +x scripts/*.sh`
3. Ejecuta el instalador: `./scripts/install.sh` (Linux) o `.\scripts\install.ps1` (Windows).

El instalador detectará el entorno, generará aleatoriamente un archivo `.env` criptográficamente seguro y levantará la arquitectura RAG al completo.
