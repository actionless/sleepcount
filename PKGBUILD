# Maintainer: Yauheni Kirylau <actionless dot loveless AT gmail.com>
# shellcheck disable=SC2034,SC2154

pkgname=sleepcount-git
pkgver=0.1.1
pkgrel=1
pkgdesc="just as a simple 'sleep' CLI util but with countdown option and HH:MM:SS target time"
arch=('any')
url="https://github.com/actionless/sleepcount"
license=('GPL3')
source=(
	"$pkgname::git+https://github.com/actionless/sleepcount.git#branch=master"
)
md5sums=(
	"SKIP"
)
depends=(
	'python'
)
optdepends=(
)
conflicts=('sleepcount')
provides=('sleepcount')

pkgver() {
	cd "${srcdir}/${pkgname}" || exit 2
	set -o pipefail
	git describe --long | sed 's/\([^-]*-g\)/r\1/;s/-/./g' || echo 0.0.1
}

build() {
	cd "${srcdir}/${pkgname}" || exit 2
}

package() {
	cd "${srcdir}/${pkgname}" || exit 2
	/usr/bin/python3 setup.py install --prefix=/usr --root="$pkgdir/" --optimize=1
	install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
	#install -Dm644 sleepcount.1 "$pkgdir/usr/share/man/man1/sleepcount.1"
	cp -r ./packaging/* "${pkgdir}"
}
