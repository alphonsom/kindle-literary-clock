# Web version (iPad and other browsers)

The same literary clock as a single web page, using the same quotes as the Kindle version.
It is written for old devices: plain ES5 JavaScript and CSS, tested for Safari on iOS 12
(first-generation iPad Air, model MD788B/A).

- every minute a quote containing the current time is shown, with the time in **bold**
- the text is scaled to fill the screen, in portrait or landscape
- **tap** to show or hide the title and author ("quiz mode")
- **long press** to switch between dark and light (dark is dimmed from 22:00 to 07:00)
- both settings are remembered on the device
- `?time=HH:MM` pins the clock to one minute, for checking how a quote looks

On a computer, a click toggles the credits, and the `c` and `t` keys toggle the credits and the theme.

## Build

The page reads `quotes.js`, which is generated from the quotes yaml. Rebuild it after changing quotes:

```
quote_to_image/venv/bin/python web/build_web.py
```

This also copies the Linux Libertine fonts to `web/fonts`.
`quotes.js` and `fonts/` are not committed: the GitHub Pages workflow builds them on every push to main.

## Serve

Any static web server will do. On a computer or Raspberry Pi on the same network:

```
python3 -m http.server 8000 --directory web
```

Then open `http://<ip-of-that-computer>:8000` on the iPad.
Over plain http the page needs that server to stay running.

Served over https, the service worker keeps a copy of everything on the device, so after the first load
the clock runs without a network and only needs it to pick up updates.
`.github/workflows/pages.yml` publishes the clock to GitHub Pages on every push to main
(enable Pages with source "GitHub Actions" in the repository settings).

## iPad setup

1. Open the page in Safari, tap the share button and choose **Add to Home Screen**.
   Started from the home screen, the clock runs full screen without Safari's toolbars.
2. **Settings → Display & Brightness → Auto-Lock → Never**
3. **Settings → General → Date & Time → Set Automatically**
4. **Settings → General → Accessibility → Guided Access**: turn it on and set a passcode.
   Open the clock, triple-click the Home button and tap Start. The iPad is now locked to the clock;
   triple-click again and enter the passcode to leave.
5. Turn on **Do Not Disturb** and set the brightness low.
6. Keep it plugged in. Check an old battery now and then for swelling.
