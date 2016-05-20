## Rtabmap_ros
[rtabmap_ros](http://wiki.ros.org/rtabmap_ros)根據RGBD資訊,提供Mapping, Localization, Visual odometry等功能. 以下將會根據主要功能提供說明

---

>**注意：** clone下來的package請在 **root** 底下運作,否則無法正常運作

---

### rtabmap_slam_v_odom.launch
這是根據rtabmap_ros內的`rgbd_mapping.launch`作簡單修改而成,主要
修改的內容有
1. 選擇localization mode

2. 使用rtabmap_ros所提供的Visual odometry

將args `"--delete_db_on_start"`去掉,並在param `database_path`選擇已建立的地圖,最後將param `Mem/IncrementalMemory`設成false.

選擇使用rtabmap_ros提供的rgbd_odometry

這個launch檔將提供`/map->/odom`與`/odom->/camera_link`的tf,與topic '/odom'

### rtabmap_slam_w_odom.launch
與rtabmap_slam_v_odom.launch相似,只是將rgbd_odometry關閉

### robot_setup_v.py
搭配rtabmap_slam_v_odom.launch使用,這邊只是單純的提供機器人的static tf,包含`/base_link->/camera_link`與`/base_link->laser_link`等感測器擺放的相對位置

### robot_setup.py
搭配rtabmap_slam_w_odom.launch使用,一樣提供`/base_link->/camera_link`與`/base_link->laser_link`的關係,由於Kobuki所提供的`/kobuki/odom`資訊其covariance太大,會導致rtabmap無法運作,因此先接收並重新publish `/odom` 同時提供`/odom->/base_link`的tf

### demo_localization.launch
主要使用了`rtabmap_slam_v_odom.launch`, `xtionpro.launch`, `robot_setup_v.py` 可以在rviz觀察到`/map->odom`的校正關係(也就是說機器人一開機時的位置odom的原點與map的原點並不一致,藉由視覺的定位提供了校正的關係),直接觀察`/map->/base_link`便可以驗證定位是否正確,若是一開始系統出現warning,可能的原因是目前的景像無法辨認出目前的定位,因此試著移動機器人將可以得到改善,或者使用`rosservice call /rtabmap/reset_odom`重新reset `rgbd_odometry`所提供的odometry

### demo_mapping.launch 
使用`rtabmap_slam_mapping.launch`將模式改成mapping mode,地圖建立在include下的temp.db,使用kobuki提供的wheel odometry提供mapping,利用遠端遙控的方式,便可以進行mapping並同時localization,temp.db檔案在關閉時將自動儲存與覆蓋,因此若想要保留此場景的資料,必須要手動移動檔案,避免程式改寫地圖內容

### nav_slam_v.launch
nav_slam_v與nav_slam_w其實是類似的,差別只在於使用wheel odometry與visual odometry來進行,`nav_slam_*`內只是多了用來產生雷射資訊的`laser_filters`與`depthimage_to _laserscan`並使用`move_base`來導航,導航的global map使用rtabmap提供的`proj_map`進行導航
