#pragma once

#include <fstream>
#include <functional>
#include <gameboycore/gameboycore.h>
#include <ios>
#include <string>
#include <vector>

class PyGameboyCore : public gb::GameboyCore
{
public:
  enum class KeyAction
  {
      PRESS, RELEASE
  };

  PyGameboyCore() = default;
  ~PyGameboyCore() = default;

  void register_scanline_callback(
    const std::function<void(const gb::GPU::Scanline&, int)>& scanline_callback
  )
  {
    scanline_callback_ = scanline_callback;
    this->getGPU()->setRenderCallback(
      std::bind(
        &PyGameboyCore::scanline_callback_fn,
        this,
        std::placeholders::_1,
        std::placeholders::_2
      )
    );
  }

  void register_vblank_callback(const std::function<void(void)>& vblank_callback)
  {
    vblank_callback_ = vblank_callback;
  }

  void input(gb::Joy::Key key, KeyAction action)
    {
        if(action == KeyAction::PRESS)
        {
            this->getJoypad()->press(key);
        }
        else
        {
            this->getJoypad()->release(key);
        }
    }

    void open(const std::string& rom_file)
    {
        std::ifstream file(rom_file, std::ios::binary | std::ios::ate);
        auto size = file.tellg();

        std::vector<uint8_t> buffer;
        buffer.resize(size);

        file.seekg(0, std::ios::beg);
        file.read((char*)&buffer[0], size);

        this->loadROM(&buffer[0], size);
    }

private:
  void scanline_callback_fn(const gb::GPU::Scanline& scanline, int line)
  {
    scanline_callback_(scanline, line);

    if (line == 143)
    {
      vblank_callback_();
    }
  }

private:
  std::function<void(gb::GPU::Scanline, int)> scanline_callback_;
  std::function<void(void)> vblank_callback_;
};
