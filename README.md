# LeagueLanguagePatch

LeagueLanguagePatch is a simple Python script designed to streamline the process of renaming WAD vo files, allowing users to enjoy voiceovers in a language different from the selected one in the League of Legends client.

## How to Use:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/LeagueLanguagePatch.git
   cd LeagueLanguagePatch
   ```
2. Install Dependencies:
Ensure you have Python installed. The script uses standard libraries, so no additional dependencies are required.
3. Download cslol-manager https://github.com/LeagueToolkit/cslol-manager/releases/latest and create an empty mod
4. Before running the script make sure to have set up your client to your desired voice over language for example Japanese, and ensure it fully patched.
5. Run the Language Patch:
Use the script to process the WAD files.

   ```bash
   python main.py --league_dir "Path/To/Your/League/Directory" --output_folder "Path/To/Your/Output/Folder" --target_region "ja_JP" --new_region "en_us"
   ```

--league_dir: Path to your League of Legends directory.

--output_folder: Path to the output folder, preferably the cslol mod's WAD folder.

--target_region: Target region of your desired voice overs (e.g., "ja_JP" for Japanese).

--new_region: New region to rename the voiceovers to (the one you want to have the setup in client for UI) (e.g., "en_us" for English).
