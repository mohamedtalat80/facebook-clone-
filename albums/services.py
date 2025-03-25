import os
import shutil

def move_photo_from_child(parent_folder_path):
    try:
        # Check if parent folder exists
        if not os.path.exists(parent_folder_path):
            print(f"Error: Parent folder '{parent_folder_path}' does not exist")
            return

        # Get list of child folders
        child_folders = [f for f in os.listdir(parent_folder_path) 
                        if os.path.isdir(os.path.join(parent_folder_path, f))]
        print(child_folders)
        if not child_folders:
            print("Error: No child folders found in parent directory")
            return

        # Use the first child folder found
        for i in range(len(child_folders)):
          child_folder = child_folders[i]
          child_folder_path = os.path.join(parent_folder_path, child_folder)
          print(child_folder_path)
          # Look for image files in child folder
          image_extensions = ('.jpg','.JPG', '.jpeg','webp', '.png', '.gif','mp4', '.bmp')
          images = [f for f in os.listdir(child_folder_path) 
                  if f.lower().endswith(image_extensions)]

          if not images:
              print("Error: No image files found in child folder")
              
              continue
            
          else:
            print (images)

        # Use the first image found
        
            image_to_move = images[0]
            print (F"the is {image_to_move}")
            source_path = os.path.join(child_folder_path, image_to_move)
            destination_path = os.path.join(parent_folder_path, image_to_move)

            # Move the image to parent folder
            shutil.move(source_path, destination_path)
            print(f"Successfully moved '{image_to_move}' to{destination_path} folder")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage with corrected path
parent_folder = r"C:\Users\hp\Desktop\New folder (2)"  # Using raw string
# OR parent_folder = "C:\\Users\\hp\\Desktop\\New folder(2)"  # Using double backslashes
# OR parent_folder = "C:/Users/hp/Desktop/New folder(2)"  # Using forward slashes
move_photo_from_child(parent_folder)