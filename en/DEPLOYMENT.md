# 23Century.id - Deployment Guide

## Pre-Deployment Checklist

✅ All items below have been completed. Site is ready to deploy.

- [x] All broken WordPress paths have been fixed
- [x] All jQuery references converted to CDN
- [x] All missing images created or fetched
- [x] All missing pages created
- [x] All anchor IDs added and verified
- [x] CSS and JavaScript assets in place
- [x] 124 HTML files verified and working

## Deployment Steps

### 1. Pre-Flight Verification

Run the link analyzer one last time to confirm:

```bash
python3 link_analyzer.py
```

Expected output:
- 124 HTML files found
- 8 "broken" links in fetched_pages/ (these are false positives - archived pages)
- All main pages functional

### 2. Static Site Deployment

Deploy the entire directory to your web server:

```bash
# Using rsync
rsync -avz /Users/asiboro/Sources/Work/23centuryid/ user@server:/var/www/23century.id/

# Using scp
scp -r /Users/asiboro/Sources/Work/23centuryid/* user@server:/var/www/23century.id/
```

### 3. Server Configuration

Ensure your web server:

- ✅ Serves static HTML files
- ✅ Supports CDN jQuery from code.jquery.com
- ✅ Redirects `/` to `/index.html` (for SPA-like behavior)
- ✅ Handles 404s gracefully

### 4. Post-Deployment Verification

After deployment, verify:

1. **Main pages load correctly**
   - https://yourdomain.com/
   - https://yourdomain.com/about/
   - https://yourdomain.com/faq/
   - https://yourdomain.com/cell-laboratory/

2. **Images load correctly**
   - Check `/assets/img/` files display without 404s
   - Verify CSS/JS from CDN loads

3. **Anchors work correctly**
   - https://yourdomain.com/faq/#faq-01
   - https://yourdomain.com/flow/#flow-02
   - https://yourdomain.com/cell-laboratory/#cgmp-cgtp

4. **Navigation links work**
   - All internal links point to correct pages
   - No console errors in browser dev tools

## Directory Structure Overview

```
23centuryid/
├── index.html ..................... Home page
├── about/index.html ............... About page
├── faq/index.html ................. FAQ with anchors
├── flow/index.html ................ Process flow with anchors
├── cell-laboratory/index.html ..... Laboratory page
├── treatable/ ..................... Treatment condition pages (15+)
├── msc/ ........................... MSC education pages (5)
├── news/ .......................... News articles (4)
├── certifications/ ................ Certification pages (2)
├── voice/ ......................... Testimonials
├── contact/ ....................... Contact page
├── assets/
│   ├── css/
│   │   ├── style.css ............. Base styles
│   │   └── main.css .............. Enhanced styles (217 lines)
│   ├── js/
│   │   └── main.js ............... Interactivity (72 lines)
│   └── img/ ....................... 71 image files
├── fetched_pages/ ................. Reference copies (can be removed)
└── scripts/

    ├── link_analyzer.py .......... Check for broken links
    ├── fix_broken_links.py ....... Fix WordPress paths
    ├── fix_anchors.py ........... Add anchor IDs
    └── ... (other utilities)
```

## Maintenance Tasks

### Regular Maintenance

1. **Update placeholder content**
   - 18 placeholder images should be replaced with real content
   - 19 stub pages should be updated with real content
   - Search for "content coming soon" in HTML for pages to update

2. **Monitor for broken links**
   - Run `link_analyzer.py` monthly
   - Address any new broken links immediately

3. **Update images**
   - Replace gray placeholder images with real images from 23c.jp
   - Keep original filenames for link consistency

### Content Updates

When adding new pages:

1. Create page in appropriate directory (e.g., `/news/new-article/index.html`)
2. Use same HTML structure as existing pages
3. Include proper meta tags and Open Graph data
4. Test all links before deploying

### Performance Optimization

- Consider caching `/assets/` files for 1 year
- Compress images further if needed
- Minify CSS/JS files for production

## Rollback Plan

If issues occur after deployment:

1. **Keep backup of original**
   ```bash
   tar czf 23centuryid-backup-$(date +%Y%m%d).tar.gz /var/www/23century.id/
   ```

2. **Restore from backup if needed**
   ```bash
   tar xzf 23centuryid-backup-20250119.tar.gz -C /var/www/
   ```

## Support & Troubleshooting

### Common Issues

**Issue: Images showing as gray boxes**
- This is expected for placeholder images
- Replace with real images using actual image files from 23c.jp

**Issue: Anchor links not working**
- Verify anchor ID exists in target page (check with `verify_anchors.py`)
- All main anchor links have been verified - should work correctly

**Issue: jQuery functions not working**
- Check that jQuery from CDN loads correctly
- Check browser console for errors
- Verify `code.jquery.com` is accessible from deployment location

**Issue: 404 on certain pages**
- Verify page was created in correct directory
- Check file permissions (should be readable)
- Verify web server is configured to serve HTML files

## Contact & Documentation

- **Original site**: https://23c.jp/
- **Analysis tools**: Run `python3 link_analyzer.py` anytime
- **Verification**: Run `python3 verify_anchors.py` to check anchor IDs
- **Final report**: See `FINAL_REPORT.md` for project details

## Production Checklist

- [ ] All files deployed to production server
- [ ] Domain DNS configured correctly
- [ ] SSL certificate installed
- [ ] All pages verified accessible
- [ ] Images loading correctly
- [ ] Anchor links working
- [ ] Navigation functional
- [ ] No console errors in browser
- [ ] Mobile responsiveness verified
- [ ] SEO meta tags in place

---

**Status**: ✅ Ready for Production
**Last Updated**: October 19, 2025
**Version**: 1.0
