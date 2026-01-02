"""
Image generation module using Seedream 4.5 API with updated API format
"""

import requests
import json
import base64
import time
import os
from pathlib import Path
from typing import List, Dict, Optional
import cv2
import numpy as np

class ImageGenerator:
    """Handles image generation using Seedream 4.5 API with updated format"""

    def __init__(self, config, interaction_manager):
        self.config = config
        self.interaction = interaction_manager
        self.api_key = config.get_api_key()  # Uses API credentials from environment
        self.api_url = config.config["api"]["image_generation_url"]

        # Mock mode configuration
        self.mock_mode = os.getenv("MOCK_API", "false").lower() == "true"
        self.mock_mode = self.mock_mode or config.config.get("mock", {}).get("enabled", False)
        self.use_sample_images = config.config.get("mock", {}).get("use_sample_images", True)
        self.sample_images_dir = config.config.get("mock", {}).get("sample_images_dir", "mock_samples")

        # Ensure output directories exist
        self.image_dir = Path(config.config["paths"]["output_dir"]) / "images"
        self.image_dir.mkdir(parents=True, exist_ok=True)

        if self.mock_mode:
            print("🧪 MOCK MODE ENABLED - Using simulated API responses")

    def preprocess_user_photo(self, input_path: str) -> str:
        """
        Preprocess user photo: only resize to max 2048x2048 if larger.
        No grayscale conversion or contrast enhancement.
        """
        print("Preprocessing user photo...")
        output_path = Path(self.config.config["paths"]["temp_dir"]) / "processed_user_photo.jpg"

        try:
            # Read image
            img = cv2.imread(input_path)
            if img is None:
                raise ValueError(f"Cannot read image: {input_path}")

            # Get original dimensions
            height, width = img.shape[:2]

            # Resize only if larger than 2048 on any dimension
            max_size = 2048
            if max(height, width) > max_size:
                scale = max_size / max(height, width)
                new_width = int(width * scale)
                new_height = int(height * scale)
                img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
                print(f"  Resized: {width}x{height} -> {new_width}x{new_height}")
            else:
                print(f"  Original size: {width}x{height} (no resize needed)")

            # Save processed image
            cv2.imwrite(str(output_path), img, [cv2.IMWRITE_JPEG_QUALITY, 95])
            print(f"✅ Photo ready: {output_path}")
            return str(output_path)

        except Exception as e:
            print(f"Error preprocessing photo: {e}")
            # Return original path if preprocessing fails
            return input_path

    def preprocess_user_photo_with_index(self, input_path: str, index: int) -> str:
        """
        Preprocess user photo with unique filename to avoid overwriting.
        Only resize to max 2048x2048 if larger.
        No grayscale conversion or contrast enhancement.
        """
        print(f"Preprocessing user photo {index+1}...")
        filename = f"processed_user_photo_{index:02d}.jpg"
        output_path = Path(self.config.config["paths"]["temp_dir"]) / filename

        try:
            # Read image
            img = cv2.imread(input_path)
            if img is None:
                raise ValueError(f"Cannot read image: {input_path}")

            # Get original dimensions
            height, width = img.shape[:2]

            # Resize only if larger than 2048 on any dimension
            max_size = 2048
            if max(height, width) > max_size:
                scale = max_size / max(height, width)
                new_width = int(width * scale)
                new_height = int(height * scale)
                img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
                print(f"  Resized: {width}x{height} -> {new_width}x{new_height}")
            else:
                print(f"  Original size: {width}x{height} (no resize needed)")

            # Save processed image
            cv2.imwrite(str(output_path), img, [cv2.IMWRITE_JPEG_QUALITY, 95])
            print(f"✅ Photo ready: {output_path}")
            return str(output_path)

        except Exception as e:
            print(f"Error preprocessing photo: {e}")
            # Return original path if preprocessing fails
            return input_path

    def _encode_image_to_base64(self, image_path: str) -> str:
        """Encode image to base64 with proper format for API"""
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        base64_str = base64.b64encode(image_data).decode('utf-8')
        return f"data:image/jpeg;base64,{base64_str}"

    def generate_single_image(self, user_photo_path: str, character: Dict, index: int) -> Optional[str]:
        """
        Generate a single image with the given character using Seedream 4.5 API
        """
        # Mock mode handling
        if self.mock_mode:
            filename = f"photo_with_{character['name'].replace(' ', '_')}_{index:03d}"
            return self._generate_mock_response(filename)

        if not self.api_key:
            print("❌ API credentials not configured. Please configure required API credentials.")
            return None

        # Encode user photo
        user_image_base64 = self._encode_image_to_base64(user_photo_path)

        # Build prompt
        full_prompt = (
            f"A fan visiting movie set, taking photo with {character['name']} on film set, {character['prompt']}. "
            f"{character.get('scene', 'movie set with crew members working, cameras and equipment visible')}. "
            f"The fan is excited to meet the movie star, standing side-by-side for photo, natural happy expression. "
            f"Movie crew in background, film set atmosphere, behind-the-scenes look. "
            f"High quality cinematic photo, 8k resolution, detailed faces, realistic lighting, authentic movie set feel."
        )

        # Get image size from config
        gen_config = self.config.config["generation"]
        width = gen_config.get("image_width", 1024)
        height = gen_config.get("image_height", 1024)
        size_str = f"{width}x{height}"

        # Prepare request payload according to API docs
        payload = {
            "model": gen_config.get("image_model", "doubao-seedream-4-5-251128"),
            "prompt": full_prompt,
            "image": user_image_base64,  # Base64 encoded image
            "size": size_str,
            "negative_prompt": (
                "blurry, distorted faces, unnatural pose, bad proportions, "
                "watermark, text, low quality, artifacts, deformed hands, extra fingers"
            ),
            "sequential_image_generation": "disabled",  # Generate single image
            "response_format": "b64_json",  # Get base64 response
            "watermark": False,  # No watermark
            "seed": int(time.time_ns() % 1000000000) + index * 7919 + hash(character['name']) % 10000
        }

        # Optional: Add guidance_scale for some models
        # Note: According to docs, Seedream 4.5 doesn't support guidance_scale
        # So we don't include it

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            # Show progress if image_count is set
            if "image_count" in self.interaction.current_state:
                self.interaction.show_progress(
                    f"Generating with {character['name']}",
                    index,
                    self.interaction.current_state["image_count"]
                )

            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()

            result = response.json()

            # Check for errors in response
            if "error" in result:
                print(f"\n❌ API error for {character['name']}: {result['error'].get('message', 'Unknown error')}")
                return None

            # Check for data array
            if "data" in result and len(result["data"]) > 0:
                # Get first image data
                image_data = result["data"][0]

                # Check if it's an error object
                if "error" in image_data:
                    print(f"\n❌ Image generation error for {character['name']}: {image_data['error'].get('message', 'Unknown error')}")
                    return None

                # Check for b64_json
                if "b64_json" in image_data:
                    # Decode and save image
                    image_bytes = base64.b64decode(image_data["b64_json"])
                    filename = f"photo_with_{character['name'].replace(' ', '_')}_{index:03d}.jpg"
                    output_path = self.image_dir / filename

                    with open(output_path, "wb") as f:
                        f.write(image_bytes)

                    print(f"\n✅ Generated: {filename}")

                    # Validate image quality
                    if self.validate_image(str(output_path)):
                        return str(output_path)
                    else:
                        print(f"⚠️ Generated image failed quality check, regenerating...")
                        # Could implement retry logic here
                        return None

                # Check for url
                elif "url" in image_data:
                    # Download from URL
                    image_url = image_data["url"]
                    filename = f"photo_with_{character['name'].replace(' ', '_')}_{index:03d}.jpg"
                    output_path = self.image_dir / filename

                    # Download image
                    img_response = requests.get(image_url, timeout=60)
                    img_response.raise_for_status()

                    with open(output_path, "wb") as f:
                        f.write(img_response.content)

                    print(f"\n✅ Generated and downloaded: {filename}")

                    if self.validate_image(str(output_path)):
                        return str(output_path)
                    else:
                        return None
                else:
                    print(f"\n❌ No image data in response for {character['name']}")
                    return None
            else:
                print(f"\n❌ No data in response for {character['name']}: {result}")
                return None

        except requests.exceptions.Timeout:
            print(f"\n⚠️ Timeout generating {character['name']}. Skipping.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"\n❌ API error for {character['name']}: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None
        except Exception as e:
            print(f"\n❌ Unexpected error for {character['name']}: {e}")
            return None

    def generate_all_images(self, user_photo_path: str, characters: List[Dict]) -> List[str]:
        """
        Generate images for all specified characters
        """
        print("\n" + "=" * 60)
        print("🖼️  Image Generation Started")
        print("=" * 60)

        # Preprocess user photo
        processed_photo = self.preprocess_user_photo(user_photo_path)

        generated_images = []
        failed_characters = []

        for i, character in enumerate(characters):
            print(f"\nGenerating image {i+1}/{len(characters)}: {character['name']}")

            image_path = self.generate_single_image(processed_photo, character, i)

            if image_path:
                generated_images.append(image_path)
                # Update state
                self.interaction.update_state("generated_images", generated_images)
            else:
                failed_characters.append(character['name'])

            # Rate limiting - wait between requests
            if i < len(characters) - 1:
                time.sleep(2)

        # Summary
        print("\n" + "=" * 60)
        print("📊 Generation Summary")
        print("=" * 60)
        print(f"✅ Successfully generated: {len(generated_images)} images")
        if failed_characters:
            print(f"❌ Failed for: {', '.join(failed_characters)}")

        # Update final state
        self.interaction.current_state["image_order"] = generated_images.copy()
        self.interaction._save_state()

        return generated_images

    def generate_portrait_images(self, user_photo: str, styles: List[Dict], count: int) -> List[str]:
        """
        Generate portrait images with different styles
        """
        print("\n" + "=" * 60)
        print("🖼️  Portrait Generation Started")
        print("=" * 60)

        # Ensure count is valid
        if count is None:
            count = 1

        # Preprocess user photo
        processed_photo = self.preprocess_user_photo(user_photo)

        generated_images = []
        failed_styles = []

        for i in range(count):
            # Cycle through styles if count > number of styles
            style = styles[i % len(styles)]
            print(f"\nGenerating portrait {i+1}/{count}: {style['name']}")

            # Build prompt for portrait
            attire_desc = style.get('attire', 'appropriate attire for style')
            pose_desc = style.get('pose', 'standard portrait pose facing camera')
            lighting_desc = style.get('lighting', 'soft studio lighting')
            background_desc = style.get('background', 'clean neutral background')
            mood_desc = style.get('mood', 'confident and professional')

            # Build comprehensive prompt with explicit instructions
            prompt = (
                f"Professional portrait photography. "
                f"{style['prompt']}. "
                f"STANDARD POSE: {pose_desc}. "
                f"IMPORTANT: Generate NEW POSE, do NOT copy or preserve the original photo's pose, posture, or body position. "
                f"IMPORTANT: Use ONLY facial features from the reference photo - ignore all clothing, background, and posture. "
                f"Generate completely new body position, pose, and background as described. "
                f"STANDARD ATTIRE: {attire_desc}. "
                f"STANDARD LIGHTING: {lighting_desc}. "
                f"STANDARD BACKGROUND: {background_desc}. "
                f"STANDARD MOOD: {mood_desc}. "
                f"High quality, detailed facial features, realistic skin texture, "
                f"8k resolution, photorealistic, perfect studio photography."
            )

            # Generate image
            image_path = self._generate_with_single_photo(
                processed_photo,
                prompt,
                f"portrait_{style['name'].replace(' ', '_')}_{i:03d}",
                i
            )

            if image_path:
                generated_images.append(image_path)
                self.interaction.update_state("generated_images", generated_images)
            else:
                failed_styles.append(style['name'])

            # Rate limiting
            if i < min(count, len(styles)) - 1:
                time.sleep(2)

        # Summary
        print("\n" + "=" * 60)
        print("📊 Generation Summary")
        print("=" * 60)
        print(f"✅ Successfully generated: {len(generated_images)} portraits")
        if failed_styles:
            print(f"❌ Failed for: {', '.join(failed_styles)}")

        self.interaction.current_state["image_order"] = generated_images.copy()
        self.interaction._save_state()

        return generated_images

    def generate_couple_images(self, photos: List[str], couple_type: Dict, count: int, background: Optional[Dict] = None) -> List[str]:
        """
        Generate couple portrait images
        """
        print("\n" + "=" * 60)
        print("🖼️  Couple Portrait Generation Started")
        print("=" * 60)

        # Preprocess photos with unique filenames
        processed_photos = []
        for i, photo in enumerate(photos):
            processed_photo = self.preprocess_user_photo_with_index(photo, i)
            processed_photos.append(processed_photo)

        generated_images = []
        failed_generations = []

        for i in range(count):
            print(f"\nGenerating couple portrait {i+1}/{count}")

            # Build prompt with couple type details
            couple_prompt = couple_type.get('prompt', 'romantic couple')
            scene = couple_type.get('scene', 'outdoor park or urban setting')
            atmosphere = couple_type.get('atmosphere', 'romantic, intimate')
            attire = couple_type.get('attire', 'coordinated outfits suitable for couple')

            # Use custom background if provided
            background_desc = ""
            if background:
                background_desc = background.get('prompt', 'natural scenery')
                print(f"  Background: {background.get('name', 'Custom')}")
            elif couple_type.get('scene'):
                background_desc = couple_type.get('scene')

            # Build comprehensive prompt with gender detection instructions
            prompt = (
                f"Two people portrait, {couple_prompt}. "
                f"CRITICAL: Extract facial features and gender from EACH input photo separately. "
                f"Person 1: Use facial features and gender from FIRST input photo only. "
                f"Person 2: Use facial features and gender from SECOND input photo only. "
                f"DO NOT assume genders - detect them from the reference photos accurately. "
                f"DO NOT default to male/female - match the actual genders in input photos. "
                f"Scene: {scene}. "
                f"Atmosphere: {atmosphere}. "
                f"Attire: {attire}. "
                f"Background: {background_desc if background_desc else 'natural scenery'}. "
                f"IMPORTANT: Position Person 1 and Person 2 correctly according to the pose description. "
                f"Generate completely new body positions, poses, and backgrounds - do NOT preserve input photo poses or environments. "
                f"Use ONLY facial features and gender from reference photos - ignore all clothing, backgrounds, and original poses. "
                f"Professional portrait photography, high quality lighting. "
                f"High quality, detailed faces, realistic skin texture, 8k resolution, photorealistic."
            )

            # Generate with multiple reference photos
            image_path = self._generate_with_multiple_photos(
                processed_photos,
                prompt,
                f"couple_portrait_{i:03d}",
                i
            )

            if image_path:
                generated_images.append(image_path)
                self.interaction.update_state("generated_images", generated_images)
            else:
                failed_generations.append(str(i+1))

            # Rate limiting
            if i < count - 1:
                time.sleep(2)

        # Summary
        print("\n" + "=" * 60)
        print("📊 Generation Summary")
        print("=" * 60)
        print(f"✅ Successfully generated: {len(generated_images)} couple portraits")
        if failed_generations:
            print(f"❌ Failed for: {', '.join(failed_generations)}")

        self.interaction.current_state["image_order"] = generated_images.copy()
        self.interaction._save_state()

        return generated_images

    def generate_family_images(self, photos: List[str], person_count: int, count: int, family_template: Optional[Dict] = None, background: Optional[Dict] = None) -> List[str]:
        """
        Generate family portrait images
        """
        print("\n" + "=" * 60)
        print("🖼️  Family Portrait Generation Started")
        print("=" * 60)

        # Use provided template or get default
        if family_template is None:
            templates = self.config.get_scenario_data('family')
            family_template = templates[0] if templates else {
                'name': 'Casual Family Portrait',
                'prompt': 'Happy family portrait with natural expressions',
                'scene': 'warm home setting',
                'atmosphere': 'warm and loving',
                'attire': 'coordinated casual family outfits'
            }

        # Preprocess photos with unique filenames
        processed_photos = []
        for i, photo in enumerate(photos):
            processed_photo = self.preprocess_user_photo_with_index(photo, i)
            processed_photos.append(processed_photo)

        generated_images = []
        failed_generations = []

        for i in range(count):
            print(f"\nGenerating family portrait {i+1}/{count}")

            # Build prompt with family template details
            template_prompt = family_template.get('prompt', 'happy family portrait')
            scene = family_template.get('scene', 'warm home setting')
            atmosphere = family_template.get('atmosphere', 'warm and loving')
            attire = family_template.get('attire', 'coordinated casual family outfits')

            # Use custom background if provided
            background_desc = ""
            if background:
                background_desc = background.get('prompt', 'warm home setting')
                print(f"  Background: {background.get('name', 'Custom')}")
            elif family_template.get('scene'):
                background_desc = family_template.get('scene')

            # Build comprehensive prompt with person identification
            people_instructions = " ".join([
                f"Person {j+1}: Extract facial features, gender, age, and appearance from input photo #{j+1} only."
                for j in range(person_count)
            ])

            # Add explicit person count instructions
            person_count_instructions = ""
            if person_count == 2:
                person_count_instructions = "Person 1 must match input photo #1. Person 2 must match input photo #2."
            elif person_count == 3:
                person_count_instructions = "Person 1 must match input photo #1. Person 2 must match input photo #2. Person 3 must match input photo #3."
            elif person_count == 4:
                person_count_instructions = "Person 1 must match input photo #1. Person 2 must match input photo #2. Person 3 must match input photo #3. Person 4 must match input photo #4."
            elif person_count == 5:
                person_count_instructions = "Person 1 must match input photo #1. Person 2 must match input photo #2. Person 3 must match input photo #3. Person 4 must match input photo #4. Person 5 must match input photo #5."
            elif person_count == 6:
                person_count_instructions = "Person 1 must match input photo #1. Person 2 must match input photo #2. Person 3 must match input photo #3. Person 4 must match input photo #4. Person 5 must match input photo #5. Person 6 must match input photo #6."

            prompt = (
                f"Family portrait with EXACTLY {person_count} people. "
                f"MUST GENERATE EXACTLY {person_count} PEOPLE - NO MORE, NO FEWER. "
                f"Each person must be clearly visible and distinct. "
                f"{template_prompt}. "
                f"{people_instructions} "
                f"CRITICAL: Extract facial features and gender from EACH input photo separately. "
                f"Detect actual genders, ages, and appearances from ALL input photos accurately. "
                f"MUST create EXACTLY {person_count} persons based on the {person_count} input photos. "
                f"{person_count_instructions} "
                f"Position all {person_count} persons correctly according to family portrait arrangement. "
                f"Scene: {scene}. "
                f"Atmosphere: {atmosphere}. "
                f"Attire: {attire}. "
                f"Background: {background_desc if background_desc else 'warm home setting'}. "
                f"IMPORTANT: Generate completely new body positions, poses, and backgrounds - do NOT preserve input photo poses or environments. "
                f"Use ONLY facial features, gender, and age from reference photos - ignore all clothing, backgrounds, and original poses. "
                f"Professional portrait photography, perfect lighting. "
                f"High quality, detailed faces, realistic skin texture, 8k resolution, photorealistic."
            )

            # Generate with multiple reference photos
            image_path = self._generate_with_multiple_photos(
                processed_photos,
                prompt,
                f"family_portrait_{i:03d}",
                i
            )

            if image_path:
                generated_images.append(image_path)
                self.interaction.update_state("generated_images", generated_images)
            else:
                failed_generations.append(str(i+1))

            # Rate limiting
            if i < count - 1:
                time.sleep(2)

        # Summary
        print("\n" + "=" * 60)
        print("📊 Generation Summary")
        print("=" * 60)
        print(f"✅ Successfully generated: {len(generated_images)} family portraits")
        if failed_generations:
            print(f"❌ Failed for: {', '.join(failed_generations)}")

        self.interaction.current_state["image_order"] = generated_images.copy()
        self.interaction._save_state()

        return generated_images

    def _generate_with_single_photo(self, user_photo: str, prompt: str, filename: str, index: int) -> Optional[str]:
        """Helper method to generate image with single reference photo"""
        # Mock mode handling
        if self.mock_mode:
            return self._generate_mock_response(filename)

        # Encode user photo
        user_image_base64 = self._encode_image_to_base64(user_photo)

        # Get image size from config
        gen_config = self.config.config["generation"]
        width = gen_config.get("image_width", 2048)
        height = gen_config.get("image_height", 2048)
        size_str = f"{width}x{height}"

        # Prepare request payload
        payload = {
            "model": gen_config.get("image_model", "doubao-seedream-4-5-251128"),
            "prompt": prompt,
            "image": user_image_base64,
            "size": size_str,
            "negative_prompt": (
                "blurry, distorted faces, unnatural pose, bad proportions, "
                "watermark, text, low quality, artifacts, deformed hands, extra fingers"
            ),
            "sequential_image_generation": "disabled",
            "response_format": "b64_json",
            "watermark": False
        }

        return self._execute_api_request(payload, filename)

    def _generate_with_multiple_photos(self, photos: List[str], prompt: str, filename: str, index: int) -> Optional[str]:
        """Helper method to generate image with multiple reference photos"""
        # Mock mode handling
        if self.mock_mode:
            return self._generate_mock_response(filename)

        # Encode all photos
        images_base64 = [self._encode_image_to_base64(photo) for photo in photos]

        # Get image size from config
        gen_config = self.config.config["generation"]
        width = gen_config.get("image_width", 2048)
        height = gen_config.get("image_height", 2048)
        size_str = f"{width}x{height}"

        # Prepare request payload with multiple reference images
        payload = {
            "model": gen_config.get("image_model", "doubao-seedream-4-5-251128"),
            "prompt": prompt,
            "image": images_base64,  # Array of base64 images
            "size": size_str,
            "negative_prompt": (
                "blurry, distorted faces, unnatural pose, bad proportions, "
                "watermark, text, low quality, artifacts, deformed hands, extra fingers"
            ),
            "sequential_image_generation": "disabled",
            "response_format": "b64_json",
            "watermark": False
        }

        return self._execute_api_request(payload, filename)

    def _execute_api_request(self, payload: Dict, filename: str) -> Optional[str]:
        """Execute API request and handle response"""
        if not self.api_key:
            print("❌ API credentials not configured. Please configure required API credentials.")
            return None

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()

            result = response.json()

            # Check for errors
            if "error" in result:
                print(f"\n❌ API error: {result['error'].get('message', 'Unknown error')}")
                return None

            # Check for data array
            if "data" in result and len(result["data"]) > 0:
                image_data = result["data"][0]

                if "error" in image_data:
                    print(f"\n❌ Image generation error: {image_data['error'].get('message', 'Unknown error')}")
                    return None

                if "b64_json" in image_data:
                    image_bytes = base64.b64decode(image_data["b64_json"])
                    output_path = self.image_dir / f"{filename}.jpg"

                    with open(output_path, "wb") as f:
                        f.write(image_bytes)

                    print(f"\n✅ Generated: {filename}.jpg")

                    if self.validate_image(str(output_path)):
                        return str(output_path)
                    else:
                        print(f"⚠️ Generated image failed quality check")
                        return None

                elif "url" in image_data:
                    image_url = image_data["url"]
                    output_path = self.image_dir / f"{filename}.jpg"

                    img_response = requests.get(image_url, timeout=60)
                    img_response.raise_for_status()

                    with open(output_path, "wb") as f:
                        f.write(img_response.content)

                    print(f"\n✅ Generated and downloaded: {filename}.jpg")

                    if self.validate_image(str(output_path)):
                        return str(output_path)
                    else:
                        return None
            else:
                print(f"\n❌ No data in response: {result}")
                return None

        except requests.exceptions.Timeout:
            print(f"\n⚠️ Timeout. Skipping.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"\n❌ API error: {e}")
            return None
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            return None

    def regenerate_image(self, user_photo_path: str, character: Dict, index: int) -> Optional[str]:
        """
        Regenerate a specific image
        """
        print(f"\n🔄 Regenerating image with {character['name']}...")
        return self.generate_single_image(user_photo_path, character, index)

    def validate_image(self, image_path: str) -> bool:
        """
        Validate generated image quality
        """
        try:
            # Skip validation in mock mode (mock images are simple solid colors)
            if self.mock_mode:
                return True

            img = cv2.imread(image_path)
            if img is None:
                return False

            # Check minimum size
            h, w = img.shape[:2]
            if w < 512 or h < 512:
                print(f"⚠️ Image too small: {w}x{h}")
                return False

            # Check blurriness (Laplacian variance)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            fm = cv2.Laplacian(gray, cv2.CV_64F).var()

            # Lowered threshold from 50 to 30 for more lenient validation
            # Values below 30 are typically genuinely blurry
            if fm < 30:
                print(f"⚠️ Image may be blurry: variance={fm:.2f} (threshold: 30)")
                return False

            return True

        except Exception as e:
            print(f"Error validating image: {e}")
            return False

    def cleanup_temp_files(self):
        """Clean up temporary files"""
        temp_dir = Path(self.config.config["paths"]["temp_dir"])
        for file in temp_dir.glob("*"):
            try:
                if file.is_file() and file.name != "generation_state.json":
                    file.unlink()
            except Exception as e:
                print(f"Warning: Could not delete {file}: {e}")
    def _generate_mock_response(self, filename: str) -> Optional[str]:
        """Generate mock response for testing without API calls"""
        if self.use_sample_images:
            # Try to use sample image if available
            sample_path = Path(self.sample_images_dir) / f"{filename}.jpg"
            if sample_path.exists():
                output_path = self.image_dir / f"{filename}.jpg"
                import shutil
                shutil.copy(sample_path, output_path)
                print(f"\n✅ Mock: Using sample image: {filename}.jpg")
                return str(output_path)

        # Generate a mock image programmatically
        print(f"\n✅ Mock: Generating test image: {filename}.jpg")

        # Create a simple mock image (colored rectangle)
        import numpy as np
        width, height = 1440, 2560  # Use configured dimensions
        img_array = np.full((height, width, 3), [100, 150, 200], dtype=np.uint8)  # Light blue
        output_path = self.image_dir / f"{filename}.jpg"
        cv2.imwrite(str(output_path), img_array)

        print(f"✅ Mock: Generated test image: {filename}.jpg")
        return str(output_path)

    def _execute_api_request_mock(self, payload: Dict, filename: str) -> Optional[str]:
        """Mock API request for testing"""
        print(f"\n🧪 MOCK REQUEST:")
        print(f"  Model: {payload.get('model', 'doubao-seedream-4.5-251128')}")
        print(f"  Prompt length: {len(payload.get('prompt', ''))}")
        print(f"  Size: {payload.get('size', '2048x2048')}")

        # Simulate API delay (faster than real API)
        delay = 0.5  # 500ms instead of 10-20 seconds
        time.sleep(delay)

        # Return mock image
        return self._generate_mock_response(filename)
