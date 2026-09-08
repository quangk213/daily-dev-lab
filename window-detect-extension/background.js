const MENU_ID = "open-on-target-monitor";

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.removeAll(() => {
    chrome.contextMenus.create({
      id: MENU_ID,
      title: "Open in my target window",
      contexts: ["link"],
    });
  });
});

async function sendUrl(rawUrl) {
  const url = new URL(rawUrl);

  if (!["http:", "https:"].includes(url.protocol)) {
    throw new Error("Only HTTP and HTTPS links are supported.");
  }

  const { targetWindowId } = await chrome.storage.session.get("targetWindowId");

  const { focusTarget = true } = await chrome.storage.local.get("focusTarget");

  if (targetWindowId == null) {
    throw new Error(
      "Open your destination window and select it using the extension icon.",
    );
  }

  let target;

  try {
    target = await chrome.windows.get(targetWindowId);
  } catch {
    throw new Error("Your target window was closed. Select another window.");
  }

  if (target.type !== "normal" || target.incognito) {
    throw new Error("Select a normal Chrome window.");
  }

  await chrome.tabs.create({
    windowId: target.id,
    url: url.href,
    active: focusTarget,
  });

  if (focusTarget) {
    if (target.state === "minimized") {
      await chrome.windows.update(target.id, {
        state: "normal",
      });
    }

    await chrome.windows.update(target.id, {
      focused: true,
    });
  }

  await chrome.storage.local.remove("lastError");
  await chrome.action.setBadgeText({ text: "" });
}

async function reportError(error) {
  const message =
    error instanceof TypeError
      ? "Could not read a valid web link."
      : error.message || "Unable to open the link.";

  await chrome.storage.local.set({ lastError: message });
  await chrome.action.setBadgeBackgroundColor({ color: "#b42318" });
  await chrome.action.setBadgeText({ text: "!" });
}

// Process requests in order to avoid creating duplicate windows.
let queue = Promise.resolve();

function enqueue(task) {
  queue = queue.then(task).catch(reportError).catch(console.error);
}

chrome.contextMenus.onClicked.addListener((info) => {
  if (info.menuItemId === MENU_ID) {
    enqueue(() => sendUrl(info.linkUrl));
  }
});

chrome.commands.onCommand.addListener((command, tab) => {
  if (command !== "send-to-monitor") return;

  enqueue(async () => {
    if (!tab?.id) {
      throw new Error("Focus a web page and try again.");
    }

    let results;

    try {
      results = await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => {
          const hovered = [...document.querySelectorAll(":hover")].pop();

          if (hovered?.tagName === "IFRAME") {
            return { useContextMenu: true };
          }

          const link = hovered?.closest("a[href], area[href]");

          if (link) {
            return { url: link.href };
          }

          if (hovered?.shadowRoot) {
            return { useContextMenu: true };
          }

          return { url: location.href };
        },
      });
    } catch {
      throw new Error(
        "Chrome blocked page access. Try a normal web page or right-click a link.",
      );
    }

    const result = results[0]?.result;

    if (result?.useContextMenu) {
      throw new Error("For this embedded link, use the right-click menu.");
    }

    if (!result?.url) {
      throw new Error("No web link or page was found.");
    }

    await sendUrl(result.url);
  });
});
