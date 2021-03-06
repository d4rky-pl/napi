#!/usr/bin/python

import datetime
import logging
import re
import xml.etree.ElementTree as ET


class XmlResult(object):

    VERSION = '2.2.0.2399'
    NAPIID = 'NapiProjekt'
    URL = 'http://pobierz.napiprojekt.pl'

    def __init__(self, subtitles = None, cover = None, movieDetails = None):
        self.logger = logging.getLogger()
        self.subtitles = subtitles
        self.movieDetails = movieDetails

        # don't set the cover if no subs
        self.cover = cover if subtitles else None

        # set "success" flag if subs provided
        self.success = True if subtitles else False

    def _makeSubtitlesElement(self, parent):
        subtitles = ET.SubElement(parent, 'subtitles')
        subtitlesId = ET.SubElement(subtitles, 'id')
        subtitlesId.text = self.subtitles.getId()

        subtitlesHash = ET.SubElement(subtitles, 'subs_hash')
        subtitlesHash.text = self.subtitles.getHash()

        filesize = ET.SubElement(subtitles, 'filesize')
        filesize.text = str(self.subtitles.getSize())

        author = ET.SubElement(subtitles, 'author')
        author.text = 'IntegrationTester'

        uploader = ET.SubElement(subtitles, 'uploader')
        uploader.text = 'IntegrationTester'

        uploadDate = ET.SubElement(subtitles, 'upload_date')
        uploadDate.text = datetime.datetime.now().strftime("%Y-%n-%d %H:%M:%S")

        self.logger.debug("Subs Id: [{}], Subs hash: [{}], Size: [{}]".format(
            subtitlesId.text, subtitlesHash.text, filesize.text))

        contents = ET.SubElement(subtitles, 'content')
        contents.text = self._makeNapiCdata(self.subtitles)

    def _makeNapiCdata(self, blob):
        return self._makeNapiCdataString(blob.getBase64())

    def _makeNapiCdataString(self, data):
        # !!! Hack Alert !!!
        # Original napi xml file holds CDATA in <>
        # which is probably wrong, but it's impossible to use these in
        # the element's test as they will be encoded into &lt; and %gt;
        #
        # These custom markers will be replaced later on once the xml is
        # produced
        return '[OPEN_TAG]' + self._makeCdata(data) + '[CLOSE_TAG]'

    def _makeCdata(self, data):
        return '![CDATA[' + data + ']]'

    def _normalizeCdata(self, xmlStr):
        def tagReplace(mathObj):
            return ('<' if mathObj.group(0) == "[OPEN_TAG]" else '>')
	# - Excuse me Sir, is this the second part of the previously
        # mentioned hack?
        # - Good eye! Yes, it is, indeed!
        return re.sub(r'\[(OPEN|CLOSE)_TAG\]',
                tagReplace, xmlStr)

    def _makeResponseTime(self, parent):
        # fake response time
        responseTime = ET.SubElement(parent, 'response_time')
        responseTime.text = '0.08 s.'

    def _makeAdvertisment(self, parent):
        advertisment = ET.SubElement(parent, 'advertisment')
        adType = ET.SubElement(advertisment, 'type')
        adType.text = 'flash'

        location = ET.SubElement(advertisment, 'flash_location_url')
        location.text = 'http://www.napiprojekt.pl/banners/show.php?id=24'

    def _makeUpdateInfo(self, parent):
        updateInfo = ET.SubElement(parent, 'update_info')

        versionNumber = ET.SubElement(updateInfo, 'version_number')
        versionNumber.text = self.VERSION

        downloadUrl = ET.SubElement(updateInfo, 'download_url')
        downloadUrl.text = 'http://pobierz.napiprojekt.pl'

        latestChanges = ET.SubElement(updateInfo, 'latest_changes')
        latestChanges.text = """&#xD;
NapiProjekt 2.2.0.2399 (2013-09-30)&#xD;
- Mo&#x17C;liwo&#x15B;&#x107; zdefiniowania kilku profil&#xF3;w pobieranych napis&#xF3;w &#xD;
- Program odporny na b&#x142;&#x119;dne nazwy folder&#xF3;w (zawieraj&#x105;ce np. niedopuszczone przez Windows znaki ':')&#xD;
- Instalator programu dodaje wyj&#x105;tek do zapory Windows (naprawa komunikacji z serwerem w niekt&#xF3;rych przypadkach)&#xD;
- Poprawione wyszukiwanie napis&#xF3;w na dysku&#xD;
&#xD;
&#xD;
NapiProjekt 2.1.1.2310 (2013-06-13)&#xD;
- Opcja automatycznego wyszukwiania napis&#xF3;w po uruchomieniu 'kolejki oczekuj&#x105;cych'&#xD;
- Poprawiono b&#x142;&#x105;d dotycz&#x105;cy znikania okienka 'kolejka oczekuj&#x105;cych'&#xD;
- Wersja portable (plik ustawienia.ini nalezy przenie&#x15B;&#x107; do katalogu z programem)&#xD;
- Likiwidacja zg&#x142;oszonych b&#x142;&#x119;d&#xF3;w&#xD;
- Program nie sprawdza braku menu 'znajd&#x17A; i dopasuj napisy' dla plik&#xF3;w '*.oga, *.ogg, *.spx, *.ram, *.ogx, *.ra'&#xD;
- Usuni&#x119;to zg&#x142;oszone b&#x142;&#x119;dy&#xD;
&#xD;"""

    def _makeCover(self, parent):
        if self.cover:
            cover = ET.SubElement(parent, 'cover')
            cover.text = self._makeNapiCdata(self.cover)

    def _makeMovieDetails(self, parent):
        title = ET.SubElement(parent, 'title')
        title.text = self._makeNapiCdataString(self.movieDetails.title)

        otherTitle = ET.SubElement(parent, 'other_titles')
        otherTitle0 = ET.SubElement(otherTitle, 'other_0')
        otherTitle0.text = self._makeNapiCdataString(self.movieDetails.otherTitle)

        year = ET.SubElement(parent, 'year')
        year.text = self.movieDetails.year

        country = ET.SubElement(parent, 'country')
        countryPl = ET.SubElement(country, 'pl')
        countryPl.text = self.movieDetails.countryPl
        countryEn = ET.SubElement(country, 'en')
        countryEn.text = self.movieDetails.countryEn

        genre = ET.SubElement(parent, 'genre')
        genrePl = ET.SubElement(genre, 'pl')
        genrePl.text = self.movieDetails.genrePl
        genreEn = ET.SubElement(genre, 'en')
        genreEn.text = self.movieDetails.genreEn

        direction = ET.SubElement(parent, 'direction')
        direction.text = self.movieDetails.direction
        screenplay = ET.SubElement(parent, 'screenplay')
        screenplay.text = self.movieDetails.screenplay
        cinematography = ET.SubElement(parent, 'cinematography')
        cinematography.text = self.movieDetails.cinematography

        links = ET.SubElement(parent, 'direct_links')
        imdb = ET.SubElement(links, 'imdb_com')
        imdb.text = self._makeNapiCdataString(self.movieDetails.imdb)
        filmweb = ET.SubElement(links, 'filmweb_pl')
        filmweb.text = self._makeNapiCdataString(self.movieDetails.filmweb)
        fdb = ET.SubElement(links, 'fdb_pl')
        fdb.text = self._makeNapiCdataString(self.movieDetails.fdb)
        stopklatka = ET.SubElement(links, 'stopklatka_pl')
        stopklatka.text = self._makeNapiCdataString(self.movieDetails.stopklatka)
        onet = ET.SubElement(links, 'onet_pl')
        onet.text = self._makeNapiCdataString(self.movieDetails.onet)
        wp = ET.SubElement(links, 'wp_pl')
        wp.text = self._makeNapiCdataString(self.movieDetails.wp)

        rating = ET.SubElement(parent, 'rating')
        rating.text = self.movieDetails.rating
        votes = ET.SubElement(parent, 'votes')
        votes.text = self.movieDetails.votes


    def _makeMovie(self, parent):
        movie = ET.SubElement(parent, 'movie')
        self._makeStatus(movie)
        if self.success:
            self._makeCover(movie)

            if self.movieDetails:
                self._makeMovieDetails(movie)

    def _makeStatus(self, parent):
        status = ET.SubElement(parent, 'status')
        status.text = 'success' if self.success else 'failed'

    def toString(self):
        result = ET.Element('result')
        self._makeMovie(result)

        if self.success:
            self._makeStatus(result)
            self._makeSubtitlesElement(result)

        self._makeAdvertisment(result)
        self._makeUpdateInfo(result)
        self._makeResponseTime(result)
        return self._normalizeCdata(ET.tostring(result, 'utf-8'))
