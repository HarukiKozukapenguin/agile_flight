#pragma once

#include <yaml-cpp/yaml.h>

#include <memory>

// -- ros
#include <cv_bridge/cv_bridge.h>
#include <image_transport/image_transport.h>
#include <ros/ros.h>

#include <filesystem>

#include "std_msgs/String.h"

// -- agilicious
#include "agilib/base/parameter_base.hpp"
#include "agilib/simulator/model_body_drag.hpp"
#include "agilib/simulator/model_init.hpp"
#include "agilib/simulator/model_motor.hpp"
#include "agilib/simulator/model_propeller_bem.hpp"
#include "agilib/simulator/model_rigid_body.hpp"
#include "agilib/simulator/model_thrust_torque_simple.hpp"
#include "agilib/simulator/quadrotor_simulator.hpp"
#include "agilib/utils/timer.hpp"
#include "agiros/ros_pilot.hpp"

// flightlib
#include "flightlib/bridges/unity_bridge.hpp"
#include "flightlib/common/command.hpp"
#include "flightlib/common/logger.hpp"
#include "flightlib/common/quad_state.hpp"
#include "flightlib/common/types.hpp"
#include "flightlib/common/utils.hpp"
#include "flightlib/envs/env_base.hpp"
#include "flightlib/envs/vision_env/vision_env.hpp"
#include "flightlib/objects/quadrotor.hpp"
#include "flightlib/objects/static_object.hpp"
#include "flightlib/sensors/rgb_camera.hpp"


namespace agi {

class VisionSim {
 public:
  EIGEN_MAKE_ALIGNED_OPERATOR_NEW
  VisionSim(const ros::NodeHandle& nh, const ros::NodeHandle& pnh);
  VisionSim() : VisionSim(ros::NodeHandle(), ros::NodeHandle("~")) {}
  ~VisionSim();

 private:
  void resetCallback(const std_msgs::EmptyConstPtr& msg);
  void loadQuadrotorCallback(const std_msgs::StringConstPtr& msg);

  void simLoop();
  void publishState(const QuadState& state);
  void publishImages(const QuadState& state);

  ros::NodeHandle nh_, pnh_;
  ros::Subscriber reset_sub_;
  ros::Subscriber reload_quad_sub_;
  ros::Subscriber reload_mockvio_sub_;
  ros::Publisher odometry_pub_;
  ros::Publisher state_pub_;
  ros::Publisher delayed_state_pub_;
  ros::Publisher mockvio_state_pub_;
  ros::Publisher clock_pub_;

  //
  image_transport::Publisher image_pub_;
  image_transport::Publisher depth_pub_;
  image_transport::Publisher opticalflow_pub_;


  Quadrotor quad_;
  QuadrotorSimulator simulator_;
  RosPilot ros_pilot_;
  Scalar sim_dt_ = 0.01;
  Scalar camera_dt_ = 0.04;  // 20 Hz. Should be a multiple of sim_dt_
  int render_every_n_steps_ = camera_dt_ / sim_dt_;
  int step_counter_ = 0;
  Scalar real_time_factor_ = 1.0;
  bool render_ = false;
  ros::WallTime t_start_;

  std::string agi_param_directory_;
  std::string ros_param_directory_;

  // flightmare vision environment
  flightlib::VisionEnv vision_env_;
  flightlib::FrameID frame_id_;

  // -- Race tracks
  Vector<3> start_pos_;
  Vector<3> goal_pos_;

  std::mutex sim_mutex_;
  std::thread sim_thread_;
  std::thread render_thread_;
};

}  // namespace agi