# Maintainer: Yauheni Kirylau <actionless dot loveless AT gmail.com>
# shellcheck disable=SC2034,SC2154

pkgname=sleepcount-git
pkgver=0.1.3
pkgrel=1
pkgdesc="just as a simple 'sleep' CLI util but with options for countdown and HH:MM:SS target time"
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
makedepends=(
	'python-wheel'
	'python-hatchling'
	'python-build'
	'python-installer'
	'python-setuptools'  # i think it normally should be required by python-pep517 which required by python-build/installer
	'python-markdown-it-py'
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
	/usr/bin/python3 -m build --wheel --no-isolation
}

package() {
	cd "${srcdir}/${pkgname}" || exit 2
	/usr/bin/python3 -m installer --destdir="$pkgdir" dist/*.whl
	install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
	#install -Dm644 sleepcount.1 "$pkgdir/usr/share/man/man1/sleepcount.1"
	cp -r ./packaging/* "${pkgdir}"
}
