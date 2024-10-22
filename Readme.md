# Topaz Photo AI integration

This extension integrates [Topaz Photo AI](https://www.topazlabs.com/topaz-photo-ai) upscaling feature into [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui). So you can use it inside *hires fix*, *upscaler_for_img2img* or in *extras* tab. You need to have Topaz Photo AI of version >= 2.1.3 (do not confuse with topaz gigapixel), and provide a path to `tpai.exe` usually located in `C:\Program Files\Topaz Labs LLC\Topaz Photo AI` in `--topaz-photo-ai-exe` cmd flag of webui

![](/images/preview.png)
![](/images/upscalers.png)

Also there are Sharpe and Denoise features in extras tab

To copy path to file in Windows, you need to press right mouse click holding "Shift" button (or not, depends on OS version), and select "Copy file as path"

<details>
<summary>
For Linux
</summary>

If you use Linux, you need to write a script, which launches `tpai.exe` via wine, with all arguments passing. E.g.

```bash
#!/bin/bash
cd "$(dirname "$0")"
export WINEDEBUG=-all
export DXVK_LOG_LEVEL=warn
wine <path to tpai.exe> "$@"
rc=$?
exit $rc
```

You can install `winetricks` and run `winetricks -q dxvk` to allow topaz to see your gpu. But it won't work because dxvk doesn't support directx12 (directml) which is required. Vkd3d in winesticks does support it partially, gpu is utilized, but the image is blured and glitched, so it isn't a proper directml support

</details>

<details>
<summary>
For portable version
</summary>

If you use a portable version of Topaz Photo AI, you need to write a wrapper script which replaces `Topaz Photo AI.exe` with `tpai.exe` and starts portable version, and set path to this script instead

For Linux:
```bash
#!/bin/bash
cd "$(dirname "$0")"
export WINEDEBUG=-all
export DXVK_LOG_LEVEL=warn
if [ ! -f 'App/Topaz Photo AI/Topaz Photo AI_.exe' ]; then
    mv 'App/Topaz Photo AI/Topaz Photo AI.exe' 'App/Topaz Photo AI/Topaz Photo AI_.exe'
    mv 'App/Topaz Photo AI/tpai.exe' 'App/Topaz Photo AI/Topaz Photo AI.exe'
fi
xvfb-run wine PhotoAIportable.exe "$@"
rc=$?
if [ ! -f 'App/Topaz Photo AI/tpai.exe' ]; then
    mv 'App/Topaz Photo AI/Topaz Photo AI.exe' 'App/Topaz Photo AI/tpai.exe'
    mv 'App/Topaz Photo AI/Topaz Photo AI_.exe' 'App/Topaz Photo AI/Topaz Photo AI.exe'
fi
exit $rc
```

`xvfb-run` is not necessary, it's used for hiding cmd.exe window. Can be installed by `sudo yay -S xorg-server-xvfb` on Arch-based, or `sudo apt install xvfb` on Ubuntu-based

For Windows a similar script will work but bad with admin right request and cmd window every time. So don't use portable version in Windows

</details>

Just in case, this extension is more about fun, and adding topaz in webui just because it's possibe. If you want to get free models with similar quality, you can use [4x-Nomos8kHAT-L-otf](https://openmodeldb.info/models/4x-Nomos8kHAT-L-otf) and [4x-FaceUpDAT](https://openmodeldb.info/models/4x-FaceUpDAT), place them into `models/DAT` directory, or even you can try [StableSR](https://github.com/pkuliyi2015/sd-webui-stablesr)

Btw in some cases Topaz shows the best quality among dedicated upscaling models. And it's significantly faster even on cpu if you need only 2x upscale of a big image
![](/images/comparation.jpg)

<details>
<summary>
but StableSR is still better
</summary>

![](/images/stablesr.jpg)

And the fastest in pair with turbo model

</details>
