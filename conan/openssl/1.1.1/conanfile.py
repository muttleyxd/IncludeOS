import shutil
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from conans import ConanFile,CMake,tools

class ProtobufConan(ConanFile):
    settings="os","compiler","build_type","arch"
    name = "openssl"
    version = "1.1.1" ##if we remove this line we can specify it from outside this script!! ps ps
    options = {"threads":[True, False]}
    tag="OpenSSL_"+version.replace('.','_')
    default_options = {"threads": False}
    #options = {"shared":False}
    #branch = "version"+version
    license = 'Apache 2.0'
    description = 'A language-neutral, platform-neutral extensible mechanism for serializing structured data.'
    url = "https://www.openssl.org"
    #exports_sources=['protobuf-options.cmake']
    #keep_imports=True
    #TODO handle build_requrements
    #def build_requirements(self):
        #self.build_requires("binutils/2.31@includeos/stable")
        #self.build_requires("musl/v1.1.18@includeos/stable")
        #self.build_requires("llvm/5.0@includeos/stable")## do we need this or just headers

    def imports(self):
        self.copy("*",dst="target",src=".")

    def source(self):
        repo = tools.Git(folder="openssl")
        repo.clone("https://github.com/openssl/openssl.git")
        self.run("git fetch --all --tags --prune",cwd="openssl")
        self.run("git checkout tags/"+str(self.tag)+" -b "+str(self.tag),cwd="openssl")

    def build(self):
        #TODO handle arch target and optimalizations
        #TODO use our own includes!
        options=" no-shared no-ssl3 enable-ubsan "
        if (not self.options.threads):
            options+=" no-threads "
        #if ()
        #self.run("./Configure --prefix="+self.package_folder+" --libdir=lib no-ssl3-method enable-ec_nistp_64_gcc_128 linux-x86_64 "+flags,cwd="openssl")
        self.run(("./config --prefix="+self.package_folder+" --openssldir="+self.package_folder+options),cwd="openssl" )
        self.run("make -j16 depend",cwd="openssl")
        self.run("make -j16",cwd="openssl")


    def package(self):
        self.copy("*.h",dst="include/openssl",src="openssl/include/openssl")
        self.copy("*.a",dst="lib",src="openssl")
        #print("TODO")
        #todo extract to includeos/include!!
        #self.copy("*",dst="include/rapidjson",src="rapidjson/include/rapidjson")

    def deploy(self):
        self.copy("*.h",dst="include/openssl",src="openssl/include/openssl")
        self.copy("*.a",dst="lib",src="openssl")
        #print("TODO")
        #self.copy("*",dst="include/rapidjson",src="include/rapidjson")
