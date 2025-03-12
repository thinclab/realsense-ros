import sys
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, OpaqueFunction, SetLaunchConfiguration
from launch.actions.include_launch_description import IncludeLaunchDescription
from launch.launch_description_sources.python_launch_description_source import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def launch_setup(context, *args, **kwargs):

    align_depth_enable = LaunchConfiguration("align_depth.enable")
    model = LaunchConfiguration("model")
    model_val = model.perform(context)
    sys.argv.append(f"model:={model.perform(context)}")

    launch_args = {
        'model' : model_val,
        }.items()

    camera_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            get_package_share_directory("realsense2_camera"),
            "/launch/rs_launch.py",
        ]),
        launch_arguments = {
            'align_depth.enable' : align_depth_enable,
        }.items(),
    )

    print(model.perform(context))

    urdf_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [get_package_share_directory("realsense2_description"), "/launch/view_model.launch.py"]
            ),
        # launch_arguments = launch_args,
    )

    to_start = [camera_launch, urdf_launch]
    return to_start


def generate_launch_description():
    launch_arguments = []
    launch_arguments.append(DeclareLaunchArgument("align_depth.enable", default_value="true"))
    launch_arguments.append(DeclareLaunchArgument("model", default_value="test_d435_camera.urdf.xacro"))
    return LaunchDescription(launch_arguments + [OpaqueFunction(function=launch_setup)])
