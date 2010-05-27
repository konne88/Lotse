# Contributor: Niklas Schnelle <niklas@komani.de>

pkgname=Lotse
pkgver=0.1
pkgrel=1
pkgdesc="A small application for geocaching written in Python"
arch=(any)
url="http://github.com/konne88/Lotse"
license=("GPL")
depends=('python' 'pygtk')
makedepends=()
provides=()
conflicts=()
replaces=()
backup=()
options=(!emptydirs)
source=(dist/$pkgname-$pkgver.tar.gz)
md5sums=('9da5fb54954436be69a4a4fa46ce8985')

build() {
  cd $srcdir/$pkgname-$pkgver 
  python setup.py install --root=$pkgdir/ --optimize=1 || return 1

  # Remember to install licenses if the license is not a common license!
  # install -D -m644 $srcdir/LICENSE $pkgdir/usr/share/licenses/$pkgname/LICENSE
}
