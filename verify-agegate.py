# -*- coding: utf-8 -*-
"""t_agegate_bypass 修复验证脚本：18+ 年龄门全站覆盖 8 项实测。

用法: python verify-agegate.py
依赖: playwright（venv 已装），Chromium 走指定路径。
"""
import asyncio
import json
import sys

from playwright.async_api import async_playwright

BASE = "https://33333344.xyz"
CHROME = r"C:/Users/junji/AppData/Local/ms-playwright/chromium-1228/chrome-win64/chrome.exe"
GOOGLEBOT_UA = (
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
)

PAGES_TO_SPOT_CHECK = [
    "/pages/jars/",
    "/pages/green-test/",
    "/pages/articles/",
]


async def _fresh_page(browser, user_agent=None):
    """每次全新 context（无 localStorage），模拟首次访问。"""
    context = await browser.new_context(
        user_agent=user_agent,
        viewport={"width": 1280, "height": 800},
    )
    page = await context.new_page()
    return context, page


async def check_overview(page):
    """返回 (has_gate, body_visibility, html_classes)。"""
    info = await page.evaluate(
        """() => {
            const overlay = document.querySelector('.ag-overlay');
            const bodyVis = document.body
                ? getComputedStyle(document.body).visibility
                : 'no-body';
            return {
                overlay: !!overlay,
                bodyVis: bodyVis,
                htmlClasses: document.documentElement.className,
            };
        }"""
    )
    return info


async def main():
    report = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=CHROME, headless=True
        )

        # ---- 1. 绕过已堵：全新上下文直链 /pages/sm-test/ ----
        ctx, page = await _fresh_page(browser)
        resp = await page.goto(BASE + "/pages/sm-test/", wait_until="domcontentloaded")
        await page.wait_for_timeout(800)
        info = await check_overview(page)
        report["1_绕过已堵"] = {
            "status": resp.status,
            "overlay": info["overlay"],
            "body_visibility": info["bodyVis"],
            "html_classes": info["htmlClasses"],
        }
        report["1_绕过已堵"]["PASS"] = (
            info["overlay"] is True
            and info["bodyVis"] == "hidden"
            and "ag-pending" in info["htmlClasses"]
        )

        # ---- 2. 过门后正常：点"我已满18岁，进入" ----
        await page.click("#ag-enter")
        await page.wait_for_timeout(500)
        info2 = await check_overview(page)
        stored = await page.evaluate(
            "() => window.localStorage.getItem('xmg_age_verified')"
        )
        content_visible = await page.evaluate(
            "() => document.body && document.body.innerText.length > 100"
        )
        report["2_过门后正常"] = {
            "overlay": info2["overlay"],
            "body_visibility": info2["bodyVis"],
            "localStorage_xmg_age_verified": stored,
            "content_len_ok": content_visible,
        }
        report["2_过门后正常"]["PASS"] = (
            info2["overlay"] is False
            and info2["bodyVis"] == "visible"
            and bool(stored)
            and content_visible is True
        )

        # ---- 3. 持久化：过门后刷新门不再出现 ----
        await page.reload(wait_until="domcontentloaded")
        await page.wait_for_timeout(800)
        info3 = await check_overview(page)
        report["3_持久化"] = {
            "overlay_after_reload": info3["overlay"],
            "body_visibility": info3["bodyVis"],
        }
        report["3_持久化"]["PASS"] = (
            info3["overlay"] is False and info3["bodyVis"] == "visible"
        )
        await ctx.close()

        # ---- 4. 首页不双入：HTML 中 age-gate.js 只出现一次 ----
        ctx, page = await _fresh_page(browser)
        await page.goto(BASE + "/", wait_until="domcontentloaded")
        html = await page.content()
        js_count = html.count("/age-gate.js")
        css_count = html.count("/age-gate.css")
        report["4_首页不双入"] = {
            "age_gate_js_count": js_count,
            "age_gate_css_count": css_count,
        }
        report["4_首页不双入"]["PASS"] = (js_count == 1 and css_count == 1)
        await ctx.close()

        # ---- 5. 多页面覆盖：3 个内容页全新上下文都有门 ----
        spot = {}
        all_pass = True
        for path in PAGES_TO_SPOT_CHECK:
            ctx, page = await _fresh_page(browser)
            r = await page.goto(BASE + path, wait_until="domcontentloaded")
            await page.wait_for_timeout(600)
            info = await check_overview(page)
            ok = (
                info["overlay"] is True
                and info["bodyVis"] == "hidden"
                and "ag-pending" in info["htmlClasses"]
            )
            spot[path] = {"status": r.status, "overlay": info["overlay"],
                          "body_visibility": info["bodyVis"], "ok": ok}
            all_pass = all_pass and ok
            await ctx.close()
        report["5_多页面覆盖"] = {"detail": spot, "PASS": all_pass}

        # ---- 6. CSP 头完好：含 nonce ----
        ctx, page = await _fresh_page(browser)
        r = await page.goto(BASE + "/pages/sm-test/", wait_until="domcontentloaded")
        csp = r.headers.get("content-security-policy", "")
        report["6_CSP头完好"] = {
            "csp_present": bool(csp),
            "has_nonce": "'nonce-" in csp,
            "csp_head": csp[:160],
        }
        report["6_CSP头完好"]["PASS"] = (bool(csp) and "'nonce-" in csp)
        await ctx.close()

        # ---- 7. 爬虫放行：Googlebot UA 无遮罩、完整 HTML ----
        ctx, page = await _fresh_page(browser, user_agent=GOOGLEBOT_UA)
        bot_results = {}
        all_bot_ok = True
        for path in ["/", "/pages/sm-test/"]:
            r = await page.goto(BASE + path, wait_until="domcontentloaded")
            await page.wait_for_timeout(600)
            info = await check_overview(page)
            text_len = await page.evaluate(
                "() => document.body ? document.body.innerText.length : 0"
            )
            ok = (info["overlay"] is False and info["bodyVis"] == "visible"
                  and text_len > 200)
            bot_results[path] = {
                "status": r.status, "overlay": info["overlay"],
                "body_visibility": info["bodyVis"], "text_len": text_len,
                "ok": ok,
            }
            all_bot_ok = all_bot_ok and ok
        report["7_爬虫放行"] = {"detail": bot_results, "PASS": all_bot_ok}
        await ctx.close()

        # ---- 8. 无 JS 报错：过门后浏览首页无 pageerror ----
        ctx, page = await _fresh_page(browser)
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        await page.goto(BASE + "/", wait_until="domcontentloaded")
        await page.wait_for_timeout(600)
        # 首页有门 → 过门
        enter = await page.query_selector("#ag-enter")
        if enter:
            await page.click("#ag-enter")
            await page.wait_for_timeout(500)
        await page.reload(wait_until="domcontentloaded")
        await page.wait_for_timeout(800)
        # 再点几个站内链接确认无运行时报错
        report["8_无JS报错"] = {"pageerrors": errors}
        report["8_无JS报错"]["PASS"] = (len(errors) == 0)
        await ctx.close()

        await browser.close()

    # ---- 汇总 ----
    all_pass = all(v.get("PASS") for v in report.values())
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("=" * 60)
    for k, v in report.items():
        print(f"{k}: {'PASS' if v.get('PASS') else 'FAIL'}")
    print("=" * 60)
    print("OVERALL:", "ALL PASS" if all_pass else "HAS FAIL")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
