import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)
    
    # Kassapaatteen luonti
    def test_luotu_kassapaate_sisaltaa_oikean_alkusaldon(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.00)
    
    def test_luotu_kassapaate_sisaltaa_oikean_maaran_edullisia(self):
        self.assertEqual(self.kassapaate.edulliset, 0)
    
    def test_luotu_kassapaate_sisaltaa_oikean_maaran_maukkaita(self):
        self.assertEqual(self.kassapaate.maukkaat, 0)

    # Käteisosto: edullinen
    def test_edullisen_kateisosto_antaa_vaihtorahan_oikein(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(1000), 760)
    
    def test_edullisen_kateisosto_lisaa_kassaan_oikean_summan(self):
        self.kassapaate.syo_edullisesti_kateisella(1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1002.40)

    def test_jos_maksu_riittava_edullisen_kateisosto_lisaa_edullisten_maaraa(self):
        self.kassapaate.syo_edullisesti_kateisella(1000)
        self.assertEqual(self.kassapaate.edulliset, 1)
    
    def test_jos_edullisen_kateismaksu_ei_riittava_kassa_ei_kasva(self):
        self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.00)

    def test_jos_edullisen_kateismaksu_ei_riittava_koko_maksu_palautetaan(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(200), 200)
    
    def test_jos_edullisen_kateismaksu_ei_riittava_edullisten_maara_ei_kasva(self):
        self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.edulliset, 0)
    
    # Käteisosto: maukas
    def test_maukkaan_kateisosto_antaa_vaihtorahan_oikein(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(1000), 600)
    
    def test_maukkaan_kateisosto_lisaa_kassaan_oikean_summan(self):
        self.kassapaate.syo_maukkaasti_kateisella(1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1004.00)

    def test_jos_maksu_riittava_maukkaan_kateisosto_lisaa_maukkaiden_maaraa(self):
        self.kassapaate.syo_maukkaasti_kateisella(1000)
        self.assertEqual(self.kassapaate.maukkaat, 1)
    
    def test_jos_maukkaan_kateismaksu_ei_riittava_kassa_ei_kasva(self):
        self.kassapaate.syo_maukkaasti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.00)

    def test_jos_maukkaan_kateismaksu_ei_riittava_koko_maksu_palautetaan(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(200), 200)
    
    def test_jos_maukkaan_kateismaksu_ei_riittava_maukkaiden_maara_ei_kasva(self):
        self.kassapaate.syo_maukkaasti_kateisella(200)
        self.assertEqual(self.kassapaate.maukkaat, 0)
    
    # Korttiosto: edullinen (oletetaan, että maksukortti toimii oikein)
    def test_kun_kortilla_riittava_saldo_edullisen_korttiosto_palauttaa_true(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti), True)

    def test_kun_kortilla_riittava_saldo_edullisten_maara_kasvaa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 1)
    
    def test_kun_kortilla_ei_riittavaa_saldoa_edullisten_maara_ei_kasva(self):
        self.maksukortti.ota_rahaa(900)
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 0)
    
    def test_kun_kortilla_ei_riittavaa_saldoa_edullisen_korttiosto_palauttaa_false(self):
        self.maksukortti.ota_rahaa(900)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti), False)
    
    def test_kortilla_maksaessa_edullisen_kassan_rahamaara_ei_muutu(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.00)

    # Korttiosto: maukas (oletetaan, että maksukortti toimii oikein)
    def test_kun_kortilla_riittava_saldo_maukkaan_korttiosto_palauttaa_true(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti), True)

    def test_kun_kortilla_riittava_saldo_maukkaiden_maara_kasvaa(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 1)
    
    def test_kun_kortilla_ei_riittavaa_saldoa_maukkaiden_maara_ei_kasva(self):
        self.maksukortti.ota_rahaa(900)
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 0)
    
    def test_kun_kortilla_ei_riittavaa_saldoa_maukkaan_korttiosto_palauttaa_false(self):
        self.maksukortti.ota_rahaa(900)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti), False)
    
    def test_kortilla_maksaessa_maukkaan_kassan_rahamaara_ei_muutu(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.00)
    
    # Maksukortin lataus
    def test_korttia_ladattaessa_kassan_rahamaara_kasvaa_ladatulla_summalla(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 500)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1005.00)
    
    def test_korttia_ladattaessa_negatiivisella_summalla_kassan_rahamaara_ei_kasva(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -500)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.00)
