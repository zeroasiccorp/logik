# umi_hello

In this example, RTL implemeted on the logik_demo eFPGA prints out a message when run in the Zero ASIC [Digital Twin Platform](https://www.zeroasic.com/emulation?demo=fpga).  Each character in the message is sent as a [UMI](https://github.com/zeroasiccorp/umi) packet to the address `0x1000000`.  Packets received at this address are interpreted as characters to be printed by the emulator.

To get started, install Logik if you haven't already:

```console
python -m pip install --upgrade logik
```

Then build the bitstream with:

```console
./umi_hello.py
```

This will take a couple of minutes, and resulting in a bitstream at `build/umi_hello/job0/convert_bitstream/0/outputs/umi_hello.bin`.  Head over to the ZA [Digital Twin Platform](https://www.zeroasic.com/emulation?demo=fpga) and follow the instructions there to simulate the bitstream.

To customize the message printed, edit the `MESSAGE` parameter in [umi_hello.v](umi_hello.v), then run `./umi_hello.py` again.
