BaiTap_AI_UET
=
Bài tập xử lý và Phân lớp Hà Nội dựa trên ảnh vệ tinh Landsat 8

Môn học Trí Tuệ Nhân Tạo - Đại học Công Nghệ, Đại học Quốc Gia Hà Nội

### Tiến độ: Kết Thúc - Huấn Luyện Dữ Liệu và Xuất Ảnh Phân Lớp

Độ Chính Xác Hiện Tại: 85%

Thuật Toán Sử Dụng: XGBoost
## Requirements
- #### Anaconda

## How To Run:
- #### Get Git Project:
    ```bash
    git clone https://github.com/Windrist/BaiTap_AI_UET
    cd BaiTap_AI_UET
    conda env create -f environment.yml
    conda activate TriTueNhanTao
    ```

- #### Download Data Folder and put on Main Folder: [Data](https://drive.google.com/drive/folders/16n4fiGjwYBzSWo5v2ELSLYHGcXnFYJpr)
- #### Change Conda Directory on main.py File:
    ```bash
    env_path = 'C:/ProgramData/Anaconda3/envs/TriTueNhanTao/Library/share/proj'  # Change Conda Directory Here!
    ```

- #### Run To get NDWI, NDVI and More Raster Indices:
    ```bash
    python main.py
    ```

- #### Check Index Rasters on Output Directory!
- #### Run to get Full Datasets with Band Values:
    ```bash
    python get_bands.py
    ```
- #### Run for Preparing Datasets using for Training:
    ```bash
    python data_prepare.py
    ```
- #### Run train.py to train and test.py to Export Image file:
    ```bash
    python train.py
    python test.py
    ```
- #### Check Image File on Output Folder!
- #### Check Documents File on Doc Folder to get more Information!
## Team

- #### Trần Hữu Quốc Đông - Trưởng nhóm
- #### Phạm Quang Hùng
- #### Hoàng Quốc Anh
- #### Nguyễn Bá Chung
- #### Ngô Thị Ngọc Quyên

### From AnChe aka BanLui Team with Love! 

