import os

# Le script magique qui force la navigation dans l'app Capacitor
script = """
<script>
document.addEventListener('click', function(e) {
  var link = e.target.closest('a');
  if (link && link.href && !link.href.startsWith('http') && !link.href.startsWith('mailto') && !link.href.startsWith('tel') && !link.href.startsWith('#')) {
    e.preventDefault();
    var page = link.getAttribute('href').replace('./', '');
    if (page) { window.location.href = page; }
  }
});
</script>
"""

for filename in os.listdir('www'):
    if not filename.endswith('.html'): continue
    filepath = os.path.join('www', filename)
    with open(filepath, 'r') as f:
        content = f.read()
    
    # On ajoute le script juste avant </body> s'il n'est pas déjà là
    if "link.href && !link.href.startsWith('http')" not in content:
        content = content.replace('</body>', script + '\n</body>')
        with open(filepath, 'w') as f:
            f.write(content)
        print('✅ Navigation corrigée pour ' + filename)
