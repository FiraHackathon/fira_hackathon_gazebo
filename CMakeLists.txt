cmake_minimum_required(VERSION 3.5)
project(fira_hackathon_gazebo)

find_package(gazebo_ros REQUIRED)
find_package(ament_cmake REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/ObstacleDetection.msg"
  DEPENDENCIES
    std_msgs
    geometry_msgs
 )

install( DIRECTORY
  worlds
  data
  DESTINATION share/${PROJECT_NAME}
)

install(PROGRAMS
  scripts/export_models_position
  scripts/generate_data_from_world
  DESTINATION lib/${PROJECT_NAME}
)

ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/env-hooks/${PROJECT_NAME}.dsv.in")

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  list(APPEND AMENT_LINT_AUTO_EXCLUDE ament_cmake_copyright)
  ament_lint_auto_find_test_dependencies()
endif()


ament_package()
