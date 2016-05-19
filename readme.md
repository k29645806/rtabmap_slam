## Rtabmap_ros
[rtabmap_ros](http://wiki.ros.org/rtabmap_ros)根據RGBD資訊,提供Mapping, Localization, Visual odometry等功能. 以下將會根據主要功能提供說明

### rtabmap_slam_v_odom.launch
這是根據rtabmap_ros內的`rgbd_mapping.launch`作簡單修改而成,主要
修改的內容有
1. 選擇localization mode

2. 使用rtabmap_ros所提供的Visual odometry

將args `"--delete_db_on_start"`去掉,並在param `database_path`選擇已建立的地圖,最後將param `Mem/IncrementalMemory`設成false.

選擇使用rtabmap_ros提供的rgbd_odometry

這個launch檔將提供`/map->/odom`的tf,與topic '/odom'

### rtabmap_slam_w_odom.launch
與rtabmap_slam_v_odom.launch相似,只是將rgbd_odometry關閉

### robot_setup_v.py
搭配rtabmap_slam_v_odom.launch使用,
