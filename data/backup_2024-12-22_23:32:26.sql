--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4 (Debian 16.4-1.pgdg120+2)
-- Dumped by pg_dump version 16.6 (Ubuntu 16.6-1.pgdg22.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: lottery_db_user
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO lottery_db_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: items; Type: TABLE; Schema: public; Owner: lottery_db_user
--

CREATE TABLE public.items (
    item_id integer NOT NULL,
    item_name character varying NOT NULL,
    item_description character varying,
    reserved_by integer,
    owner_id integer NOT NULL,
    bought boolean
);


ALTER TABLE public.items OWNER TO lottery_db_user;

--
-- Name: items_item_id_seq; Type: SEQUENCE; Schema: public; Owner: lottery_db_user
--

CREATE SEQUENCE public.items_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.items_item_id_seq OWNER TO lottery_db_user;

--
-- Name: items_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: lottery_db_user
--

ALTER SEQUENCE public.items_item_id_seq OWNED BY public.items.item_id;


--
-- Name: settings; Type: TABLE; Schema: public; Owner: lottery_db_user
--

CREATE TABLE public.settings (
    key character varying NOT NULL,
    value json NOT NULL
);


ALTER TABLE public.settings OWNER TO lottery_db_user;

--
-- Name: users; Type: TABLE; Schema: public; Owner: lottery_db_user
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    name character varying NOT NULL,
    username character varying NOT NULL,
    password character varying NOT NULL,
    visible boolean,
    choosable boolean,
    spouse integer,
    assignment integer,
    assigned_to integer,
    admin boolean,
    wishlist json,
    reserved_items json
);


ALTER TABLE public.users OWNER TO lottery_db_user;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: lottery_db_user
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO lottery_db_user;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: lottery_db_user
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: items item_id; Type: DEFAULT; Schema: public; Owner: lottery_db_user
--

ALTER TABLE ONLY public.items ALTER COLUMN item_id SET DEFAULT nextval('public.items_item_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: lottery_db_user
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: items; Type: TABLE DATA; Schema: public; Owner: lottery_db_user
--

COPY public.items (item_id, item_name, item_description, reserved_by, owner_id, bought) FROM stdin;
13	Buty do treningu siłowego	Numer referencyjny na stronie Decathlon to 8915015, rozmiar 39	\N	9	f
25	Materac rehabilitacyjny do ćwiczeń skladany	https://erli.pl/produkt/materac-gimnastyczny-rehabilitacyjny-195x80x6-mata,153067283	5	10	f
2	Strój kąpielowy jednoczęściowy	Kolor np niebieski lub czarnyy	\N	2	f
3	Pasek do spodni	Czarny, ala skórzany, fajnie jakby był z klamrą	\N	2	f
20	Karta podarunkowa do sklepu Le collet		\N	6	f
21	Perfumy Black Opium lub La vie est belle		\N	6	f
22	Spodnie, kurtka albo rękawiczki (ciepłe) do jazdy konnej		\N	6	f
23	Bokserki L	Dobrej jakości, 100 bawelna	\N	11	f
27	Koszulka na siłownię M	Taką koszulka ze sklepu sportowego jak Nike, 4f, itd. To musi być taka luźna koszulka co jak się na siłowni spółce to będzie ją łatwo zdjęć, bo się nie przykleja tak mocno do skóry. Kolor dowolny.	\N	11	f
26	Karta podarunkowa do DOUGLAS		\N	10	f
28	Stacja ładowania dla komórki i smartwatch		\N	10	f
7	Voucher na pilates na maszynach	https://app.fitssey.com/reforme/frontoffice/pricing/classes                     pilatesstudiomartaskorek.com	6	4	f
29	Dietetyka sportowa	Książka	\N	9	f
19	Kapcie Emu Mayberry lub z Stella Soft z Owca Sklep + rękawiczki boucle brązowe		3	6	t
42	Podkładka pod klawiaturę szara filcowa 80-100x 40 cm	Szerokość 80 90 lub 100 cm Przykładowa https://allegro.pl/oferta/filcowa-podkladka-pod-mysz-czarno-szara-odporna-na-zarysowania-100-40cm-16879736669	\N	7	f
52	Wanna do morsowania virtufit Decathlon		4	7	t
30	Koszulki T shirt	Firmy typu timbaland, Massimo dutti. Koszulki jednolite. Rozmiar L, fit	\N	11	f
31	Karta do Massimo dutti		\N	11	f
15	Świeczki	Ładnie pachnące	6	9	f
35	Skarpetki męskie duże	Rozmiar jakoś tak 43-47, kolorowe, mogą być tematyczne, typu jakieś ze Star Wars, Wiedźmina, mogą mieć wzory matematyczne itp	\N	1	f
37	T-shirt XXL	Czarny, bez nadruku lub z nadrukiem. Jeśli z nadrukiem, to ważne żeby był jakiś kolorowy, z tematyki to klasycznie Star Wars, Władca Pierścieni itd. może być też jakiś artysta muzyczny, typu AC/DC albo Bob Marley	\N	1	f
40	Hamulec tarczowy Shimano XT bl-8000/br 8000	Przykładowy zestaw ma w sobie klamkę hamującą i zacisk dlatego w nazwie są dwa oznaczenia bl-8000 i br-8000 może być wyższy nr jak będzie w podobnej cenie np 8100...  https://www.centrumrowerowe.pl/hamulec-tarczowy-shimano-deore-xt-br-m8000-pd3291/?v_Id=158550	\N	7	f
39	Tylko dla nadgorliwych!: Słuchawki sony xm4	Mogą być czarne albo niebieskie https://www.x-kom.pl/p/647718-sluchawki-bezprzewodowe-sony-wh-1000xm4b-czarne.html	\N	7	f
51	Książka wiedźmin rozdroże krukow	Nowa książka o wiedźminie pod tytułem rozdroże krukow.	1	11	t
11	Bransoletka	W złotym kolorze, delikatna	7	9	f
36	Lego	Jakiś mały zestaw, najlepsze są z LEGO Star Wars i Lord Od The Rings	7	1	f
6	Masaż kobido		\N	4	f
8	Koszula/le	Biała,niebieska ,wrzos	\N	8	f
46	Voucher/karta podarunkowa do sklepu „torty torty”	tortytorty.pl	\N	4	f
16	Srebrny łańcuszek	ㅤ	5	2	f
14	Balaclava	Kolor czarny, najlepiej se sznureczkami	\N	9	f
45	Ładowarka sieciowa 100W	Bez kabla dodatkowego, który by ją przedłużał, klasyczna ścienna, najlepiej Baseus. Przykładowy link: https://allegro.pl/oferta/ladowarka-sieciowa-baseus-gan5-pro-usb-c-usb-100w-czarna-kabel-1m-16882756344 Im więcej wejść tym lepiej	4	1	t
10	Organizer na kolczyki i biżuterię	coś w tym stylu :) https://allegro.pl/oferta/kuferek-szkatulka-organizer-pudelko-na-bizuterie-i-kolczyki-eleganckie-ca7-15288876860	10	2	t
49	Aparat zabawkowy		6	14	f
50	Zestaw z jednorożcem i zjezdzalnia	Np „My little Pony” jakiś mini domek albo mini zamek	\N	14	f
44	Szczoteczka do zębów	Elektryczna	6	1	f
4	Kurs z monoporcji lub tortów	Chodzi o przygotowywanie, cały proces, przy tortach może być tylko dekoracja, może być calosc	\N	4	f
32	Światło logitech litra glow	https://www.logitech.com/pl-pl/products/lighting/litra-glow.946-000002.html	6	11	f
17	Płyta indukcyjna	Przenośna, dwupalnikowa, szeroka, ale niezbyt głęboka, bo muszę ją postawić na parapecie, który ma głębokość 40 cm	10	1	t
38	Opona rowerowa	Opona MAXXIS Ardent Race 29'' szerokość 2.2'' przykładowy link do dobrego sklepu https://www.centrumrowerowe.pl/opona-maxxis-ardent-race-pd1371/?v_Id=86020	10	7	t
41	Plecak turystyczny queshua nh 500	Szary Plecak z dekatlona https://www.decathlon.pl/p/plecak-turystyczny-quechua-nh500-escape-rolltop-23-litry/_/R-p-334561	10	7	t
53	Materac KiddyMoon	Amelka chciałaby taki materac żeby mogła zabierać go na nocowanki w szkole, kiedy koleżanki do niej przychodzą oraz który na codzień służyłby jako fotel	\N	15	f
57	Zegarek ze stoperem	Fajny	\N	15	f
9	Piżama niebieska/wrzos spodnie w kraty	Bawełna długi rękaw	4	8	t
12	Bloom	Suplement, smak oryginal	10	9	t
47	Klocki magnetyczne	Magnetic, Connectix	10	14	t
54	Ładny strój kąpielowy, kolor nie czarny	Rozmiar 140	\N	15	f
56	Walizka	Wittchen kabinowa z flamingiem	2	15	t
24	Skarpetki 43	Klasyczne, ale z jakimś kolorem albo paskiem czy innym wzorem żeby można je było w praniu znaleźć i dopasować. Nie całe w jednym kolorze, ani nie całe we wzory. Po prostu jakiś wzorek mniejszy czy kolor żeby było wiadomo że to para.	\N	11	f
48	Mikroskop	https://www.empik.com/super-mikroskop-clementoni,p1360856573,zabawki-p?utm_source=google&utm_medium=cpc&utm_campaign=20422030007&utm_id=20422030007&utm_term=empik_zabawki&gclsrc=aw.ds&gad_source=1&gbraid=0AAAAADwt86ejhV9s-qyNB7U0nPJZpjper&cls=1	2	14	t
5	Piżama	Krótki rękaw, krótkie spodenki (nie musi być świąteczna)	3	2	f
43	Patera obrotowa do tortu (nie plastikowa)	Średnica min 30cm	1	4	t
1	Okulary do pływania	Takie, żeby nie przeciekały 😍	1	2	t
60	Strój na tenisa	Nie wiem dokładnie o co mu chodzi, ale na kortach jest sklep sportowy gdzie są stroje sportowe i taki jakiś mu się zamarzył	\N	16	f
61	Torba sportowa	Na tenisa, basen i inne	\N	16	f
64	LEGO 60417		\N	16	f
68	LEGO 42165		\N	16	f
69	Walizka na pilot	Staś marzy o walizce zdalnie sterowanej. Którą będzie mógł kierować będąc na lotnisku (kazał wpisać)	\N	16	f
55	Stajnia Schleich	Numer 42344	10	15	t
65	LEGO 60439		5	16	f
58	Spotkanie z Mikołajem		2	15	t
59	Rakieta do tenisa	Wysoki priorytet	\N	16	f
63	Zegarek ze stoperem	Najwyższy priorytet	\N	16	f
66	LEGO 60426		\N	16	f
67	LEGO 60396		\N	16	f
62	Tort hot wheels	Atak rekina - wysoki priorytet	10	16	f
70	Pianinko zabawkowe, ale nie organki	https://allegro.pl/oferta/duze-drewniane-pianinko-magiczne-z-ksiazeczka-do-nauki-instrument-fortepian-16514175512	10	17	t
77	Bon do Nike		\N	3	f
78	Stacja ładująca Steam Deck (Becia może się złożyć)	https://www.steamdeck.com/pl/dock	\N	3	f
73	Naklejki wielokrotnego użytku	https://www.empik.com/melissa-doug-wokol-domu-naklejki-melissa-doug,p1102873433,szkolne-i-papiernicze-p     https://www.empik.com/melissa-doug-naklejki-ksiezniczka-melissa-doug,p1105542817,szkolne-i-papiernicze-p	\N	17	f
72	Naklejki z jednorozcem	https://www.empik.com/melissa-doug-naklejki-jednorozec-uzupelnienie-300-sticker-wow-melissa-doug,p1464213092,szkolne-i-papiernicze-p	\N	17	f
74	Świąteczny kubek	Taki do zimowej herbatki  Pod kocyk i książka 🥰	4	2	t
18	Szczotka prostująca do włosów	Albo nawet lepiej od szczotki coś takiegohttps://hairtastique.com/products/airstyler-5-en-1-hairtastique?variant=50618850509140&utm_source=facebook&utm_medium=paid&tw_source=ig&tw_adid=120215431816470646&fbclid=PAY2xjawG88RZleHRuA2FlbQEwAGFkaWQBqxdMaKrZNgGmws5-n0GHL7qAjWHD1R9g0FBjMFO4YgGUe4IfbAAGHIVPPq3lVToc4kDA_aem_E9MUTv4B8on44xlC7HlB0g	\N	6	f
33	Kettlebell 20kg	Zależy mi żeby były czymś powlekane, jakaś guma albo plastikiem. Nie mają być gołe stalowe. Jeden kettlebell będzie super. 2 sztuki będą ekstra 🫶	2	11	t
76	Kontroler Xbox X	https://www.mediaexpert.pl/gaming/kontrolery-pady/przeznaczenie_xbox-series-x	7	3	f
34	Okulary do Pływania		7	3	f
75	Książka Cujo - Stephen King		2	3	f
71	Aparat zabawkowy z funkcją drukowania		4	17	f
\.


--
-- Data for Name: settings; Type: TABLE DATA; Schema: public; Owner: lottery_db_user
--

COPY public.settings (key, value) FROM stdin;
LOTTERY_ACTIVE	true
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: lottery_db_user
--

COPY public.users (user_id, name, username, password, visible, choosable, spouse, assignment, assigned_to, admin, wishlist, reserved_items) FROM stdin;
0	Admin	master	master_password	f	f	\N	\N	\N	t	[]	[]
16	Staś	Staś	1234	t	f	\N	\N	\N	f	[59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]	[]
4	Magda w	Magda	adgaM	t	t	7	8	6	f	[4, 6, 7, 43, 46]	[9, 74, 52, 45, 71]
17	Misia W	Misia	Mi$ia	t	f	\N	\N	\N	f	[70, 71, 72, 73]	[]
10	Gosia	gosiaprus@gmail.com	1234567	t	t	8	7	5	f	[26, 28, 25]	[41, 38, 10, 17, 55, 62, 12, 70, 47]
9	Marysia 	Marysia Rumianek	Prezencik#13	t	f	\N	\N	\N	f	[11, 12, 14, 13, 15, 29]	[]
5	Anna Rumianek 	Ania	22021992	t	t	12	10	11	f	[]	[16, 65, 25]
14	Marcela W	Marcela	Mar$ia	t	f	\N	\N	\N	f	[47, 48, 49, 50]	[]
12	Andrzej Rumianek	Andrzej	1234	t	t	5	2	8	f	[]	[]
11	Piotr Prus 	Piotr	piotr	t	t	6	5	2	f	[23, 24, 27, 30, 31, 32, 33, 51]	[]
6	Kaja	Kaja	kaja	t	t	11	4	3	f	[18, 19, 20, 21, 22]	[15, 7, 49, 44, 32]
8	Jurek Prus 	Jurek Prus 	Beatka11!	t	t	10	12	4	f	[8, 9]	[]
13	Gienia Rumianek	Gienia	Gi3ni4	t	f	\N	\N	\N	f	[]	[]
15	Amelka	Amelka	1234	t	f	\N	\N	\N	f	[53, 54, 55, 56, 57, 58]	[]
1	Paweł	Horacjusz	x8uhKJJh8dcRe6T	t	f	\N	\N	\N	f	[17, 35, 36, 37, 44, 45]	[1, 43, 51]
3	Bartek	Bartek	1q2w3e4r	t	t	2	6	7	f	[34, 76, 77, 75, 78]	[19, 5]
7	Mateusz 	Mateusz	haslomaslo	t	t	4	3	10	f	[38, 39, 40, 41, 42, 52]	[11, 36, 76, 34]
2	Beata	Beata Bizoń 	1234	t	t	3	11	12	f	[1, 2, 3, 5, 10, 16, 74]	[33, 56, 58, 48, 75]
\.


--
-- Name: items_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lottery_db_user
--

SELECT pg_catalog.setval('public.items_item_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lottery_db_user
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, false);


--
-- Name: items items_pkey; Type: CONSTRAINT; Schema: public; Owner: lottery_db_user
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_pkey PRIMARY KEY (item_id);


--
-- Name: settings pk_settings; Type: CONSTRAINT; Schema: public; Owner: lottery_db_user
--

ALTER TABLE ONLY public.settings
    ADD CONSTRAINT pk_settings PRIMARY KEY (key);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: lottery_db_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: lottery_db_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: items items_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: lottery_db_user
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(user_id);


--
-- Name: items items_reserved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: lottery_db_user
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_reserved_by_fkey FOREIGN KEY (reserved_by) REFERENCES public.users(user_id);


--
-- Name: users users_spouse_fkey; Type: FK CONSTRAINT; Schema: public; Owner: lottery_db_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_spouse_fkey FOREIGN KEY (spouse) REFERENCES public.users(user_id);


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON SEQUENCES TO lottery_db_user;


--
-- Name: DEFAULT PRIVILEGES FOR TYPES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TYPES TO lottery_db_user;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON FUNCTIONS TO lottery_db_user;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TABLES TO lottery_db_user;


--
-- PostgreSQL database dump complete
--

