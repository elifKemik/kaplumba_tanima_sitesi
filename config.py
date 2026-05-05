"""
Centralized configuration for Turtle Identification System
Tüm magic number'lar burada tanımlanıyor
"""

class ImageAnalysisConfig:
    """Image quality analysis thresholds"""
    MIN_BRIGHTNESS = 50                    # Çok karanlık limit
    MAX_BRIGHTNESS = 220                   # Çok parlak limit
    MIN_SHARPNESS_CRITICAL = 0.5          # Kritik netlik (image okunamaz)
    MIN_SHARPNESS_ACCEPTABLE = 2.0        # Kabul edilebilir netlik
    MIN_SHARPNESS_GOOD = 10.0             # İyi netlik
    

class ValidationConfig:
    """File validation thresholds"""
    MAX_FILE_SIZE = 5 * 1024 * 1024       # 5MB max file size
    ALLOWED_EXTENSIONS = ('.jpg', '.png', '.jpeg')  # Supported formats
    

class ModelConfig:
    """Model training and prediction configuration"""
    # Model paths
    MODEL_PATH = "yolov8n-cls.pt"  # küçük model, hızlı hesaplar
    TRAINED_MODEL_PATH = "yolo_trained.pt"
    EMBEDDINGS_PATH = "yolo_embeddings.npy"
    CNN_MODEL_PATH = "turtle_model.h5"
    CNN_EMBEDDINGS_PATH = "embeddings.npy"
    
    # Training parameters
    EPOCHS = 30
    BATCH_SIZE = 16
    IMG_SIZE = 224
    EMBEDDING_DIM = 512
    
    # Prediction thresholds
    YOLO_PREDICTION_THRESHOLD = 0.35     # YOLO model confidence threshold
    CNN_PREDICTION_THRESHOLD = 0.60       # CNN model similarity threshold
    FINAL_CONFIDENCE_THRESHOLD = 0.45     # Final identification confidence
    
    # Histogram matching
    HISTOGRAM_BINS = 8
    HISTOGRAM_RANGE = [0, 256]
    

class IdentificationConfig:
    """Identification agent configuration"""
    NORMALIZATION_FACTOR = 30             # Sharpness normalization coefficient
    ACCURACY_THRESHOLD = 50                # Minimum accuracy for identification
    CACHE_ENABLED = True                   # Enable/disable image ID caching
    

class EmbeddingConfig:
    """Embedding computation configuration"""
    SAMPLE_RANDOM = True                   # Use random sample or first image
    MIN_SAMPLES_PER_CLASS = 1              # Minimum images per turtle class
    COSINE_SIMILARITY_THRESHOLD = 0.60    # Similarity threshold for matching
    

# Convenience access
class Config:
    """Unified configuration access"""
    # Image analysis
    IMAGE_ANALYSIS = ImageAnalysisConfig()
    
    # File validation
    VALIDATION = ValidationConfig()
    
    # Model configuration
    MODEL = ModelConfig()
    
    # Identification
    IDENTIFICATION = IdentificationConfig()
    
    # Embedding
    EMBEDDING = EmbeddingConfig()
    
    # Direct access to common values
    CONFIDENCE_THRESHOLD = ModelConfig.FINAL_CONFIDENCE_THRESHOLD
    EPOCHS = ModelConfig.EPOCHS
    BATCH_SIZE = ModelConfig.BATCH_SIZE
    IMG_SIZE = ModelConfig.IMG_SIZE
    MODEL_PATH = ModelConfig.MODEL_PATH
    TRAINED_MODEL_PATH = ModelConfig.TRAINED_MODEL_PATH
