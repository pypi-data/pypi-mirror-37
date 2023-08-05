// This file is part of servoarray.
//
// servoarray is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// servoarray is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with servoarray.  If not, see <http://www.gnu.org/licenses/>.

#include "servoarray/servoarray.h"

#include <cmath>

namespace ServoArray {

ServoArray::ServoArray(std::uint8_t bus, std::uint8_t address, std::uint16_t min_pulse, std::uint16_t max_pulse)
  : driver(PCA9685(bus, address)), min_pulse(min_pulse), max_pulse(max_pulse) {
  this->values.resize(this->driver.num_servos());
}

void ServoArray::set(std::uint8_t index, double rad) {
  this->values[index] = rad;

  const auto pulse = (rad + M_PI / 2) * (this->max_pulse - this->min_pulse) / M_PI + this->min_pulse;
  this->driver.set_pwm(index, 0, pulse);
}

double ServoArray::get(std::uint8_t index) {
  if (index >= this->driver.num_servos()) {
    throw std::out_of_range("Channel index out of bounds");
  }
  return this->values[index];
}

std::uint8_t ServoArray::size() {
  return this->driver.num_servos();
}

}
