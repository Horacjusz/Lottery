PGDMP                  
    |         
   lottery_db    16.4 (Debian 16.4-1.pgdg120+2)     16.6 (Ubuntu 16.6-1.pgdg22.04+1)     3           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            4           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            5           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            6           1262    16389 
   lottery_db    DATABASE     u   CREATE DATABASE lottery_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF8';
    DROP DATABASE lottery_db;
                lottery_db_user    false            7           0    0 
   lottery_db    DATABASE PROPERTIES     3   ALTER DATABASE lottery_db SET "TimeZone" TO 'utc';
                     lottery_db_user    false                        2615    2200    public    SCHEMA     2   -- *not* creating schema, since initdb creates it
 2   -- *not* dropping schema, since initdb creates it
                lottery_db_user    false            �            1259    16422    items    TABLE     �   CREATE TABLE public.items (
    item_id integer NOT NULL,
    item_name character varying NOT NULL,
    item_description character varying,
    reserved_by integer,
    owner_id integer NOT NULL,
    bought boolean
);
    DROP TABLE public.items;
       public         heap    lottery_db_user    false    5            �            1259    16421    items_item_id_seq    SEQUENCE     �   CREATE SEQUENCE public.items_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.items_item_id_seq;
       public          lottery_db_user    false    219    5            8           0    0    items_item_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.items_item_id_seq OWNED BY public.items.item_id;
          public          lottery_db_user    false    218            �            1259    16414    settings    TABLE     ^   CREATE TABLE public.settings (
    key character varying NOT NULL,
    value json NOT NULL
);
    DROP TABLE public.settings;
       public         heap    lottery_db_user    false    5            �            1259    16399    users    TABLE     c  CREATE TABLE public.users (
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
    DROP TABLE public.users;
       public         heap    lottery_db_user    false    5            �            1259    16398    users_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.users_user_id_seq;
       public          lottery_db_user    false    5    216            9           0    0    users_user_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;
          public          lottery_db_user    false    215            �           2604    16425    items item_id    DEFAULT     n   ALTER TABLE ONLY public.items ALTER COLUMN item_id SET DEFAULT nextval('public.items_item_id_seq'::regclass);
 <   ALTER TABLE public.items ALTER COLUMN item_id DROP DEFAULT;
       public          lottery_db_user    false    219    218    219            �           2604    16402    users user_id    DEFAULT     n   ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);
 <   ALTER TABLE public.users ALTER COLUMN user_id DROP DEFAULT;
       public          lottery_db_user    false    216    215    216            0          0    16422    items 
   TABLE DATA           d   COPY public.items (item_id, item_name, item_description, reserved_by, owner_id, bought) FROM stdin;
    public          lottery_db_user    false    219   O"       .          0    16414    settings 
   TABLE DATA           .   COPY public.settings (key, value) FROM stdin;
    public          lottery_db_user    false    217   )       -          0    16399    users 
   TABLE DATA           �   COPY public.users (user_id, name, username, password, visible, choosable, spouse, assignment, assigned_to, admin, wishlist, reserved_items) FROM stdin;
    public          lottery_db_user    false    216   6)       :           0    0    items_item_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.items_item_id_seq', 1, false);
          public          lottery_db_user    false    218            ;           0    0    users_user_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.users_user_id_seq', 1, false);
          public          lottery_db_user    false    215            �           2606    16429    items items_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_pkey PRIMARY KEY (item_id);
 :   ALTER TABLE ONLY public.items DROP CONSTRAINT items_pkey;
       public            lottery_db_user    false    219            �           2606    16420    settings pk_settings 
   CONSTRAINT     S   ALTER TABLE ONLY public.settings
    ADD CONSTRAINT pk_settings PRIMARY KEY (key);
 >   ALTER TABLE ONLY public.settings DROP CONSTRAINT pk_settings;
       public            lottery_db_user    false    217            �           2606    16406    users users_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            lottery_db_user    false    216            �           2606    16408    users users_username_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
       public            lottery_db_user    false    216            �           2606    16435    items items_owner_id_fkey    FK CONSTRAINT     ~   ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(user_id);
 C   ALTER TABLE ONLY public.items DROP CONSTRAINT items_owner_id_fkey;
       public          lottery_db_user    false    216    3219    219            �           2606    16430    items items_reserved_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_reserved_by_fkey FOREIGN KEY (reserved_by) REFERENCES public.users(user_id);
 F   ALTER TABLE ONLY public.items DROP CONSTRAINT items_reserved_by_fkey;
       public          lottery_db_user    false    216    3219    219            �           2606    16409    users users_spouse_fkey    FK CONSTRAINT     z   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_spouse_fkey FOREIGN KEY (spouse) REFERENCES public.users(user_id);
 A   ALTER TABLE ONLY public.users DROP CONSTRAINT users_spouse_fkey;
       public          lottery_db_user    false    216    3219    216                        826    16391     DEFAULT PRIVILEGES FOR SEQUENCES    DEFAULT ACL     V   ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON SEQUENCES TO lottery_db_user;
                   postgres    false                       826    16393    DEFAULT PRIVILEGES FOR TYPES    DEFAULT ACL     R   ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TYPES TO lottery_db_user;
                   postgres    false                       826    16392     DEFAULT PRIVILEGES FOR FUNCTIONS    DEFAULT ACL     V   ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON FUNCTIONS TO lottery_db_user;
                   postgres    false            �           826    16390    DEFAULT PRIVILEGES FOR TABLES    DEFAULT ACL     S   ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TABLES TO lottery_db_user;
                   postgres    false            0   �  x�mV�n���k����zo�=�`iF�{��M����j�UD�8����D�W;�&��`�l�_��O��l�XP�$o�ǹ�[�#1�BC���5vUQi�{W��\{��N�j6�!+��Y��R+֙��_LO&ӓy��Fz:�?�����T,�^z���e����V��?�d�[�����lMJ���Z�˪{jdr���Q��&�LFo�;������ 	mv��d:{;'�-M?�G���p�����62�Kr��H*\��oT��%��}h��q��/��o��t��fD�\��n����;�sJ�2��յ�>�Z�7�G�D�&q�d�E����2P�m��G�Q�2������*U��4e��ŢU�)���>*�m�QZ��K-���3����������%֩v��}V/ĕ˜'[p�K���PV-I�mj�}9���)�)��5�M4�������J~��A}@��������q%�?����R{�Ĩ--���q���nj��H�V�#��c*k�Z��t��K�m��C���!6T�ʦ�8&�>*�֤\��p80���UyC�L��n
S�1�kI�$wg��^�=���܊ȵ�	��ݽ~��7�Mn�՛��KK�a}-.�҃���qg4�Lh)k�Y{�͟��w2h/Fq-�&3A�Q��8��~�!�>p���m�!E��8�sD���F���[�	�!�=�C�M�:��0�!�GyU���ɬ�~��gOjw��0/����/ݽ�,��c�2O��0���>n?���l���AV�P���)�v���ȋ�r�mF�N�?.o�{���>�& �Hb7�0̸�����U-��p�B\thPo��WH��{J�މ��ʤ�����g�@;0#}�|I%L��_�F=Nʉ�~��fF��G�Dc��P�a�Af�b�J_�t���U&�FAxz��f����� ��w\-$&�m�XI���u�UeC�6�W�9"w����7�ޠ(xA��O#����5LYc�0�k94���
ݻu����aLm��Db�\��g��bЪ��;�R!����cqU�E��:�Emvr�"��7kޑ��Z9�-�I�>�Q������`�2�[	�N�g�^~S2s����bN��g��k���x�Lh0d��KH�MP��4�'�B0���T�jL��_�Uz�5��GӞ���x�Y���\�Vp����c�a#�uE��x\��h�}�\>.�a��HR�P�3�Z�
���ώ.�O�����!�A�BB�Y7i6IW��L�'˼�e�0S�pu�3gA�7�*�U� ��a��X�K����1�� �k��g�hK�!�^eʪ��*�P���{��i�0����}H�����>�,v��'��tO2ǰc����D�`���~ԖW s����g\` /F��~�B�K�=��K�8�gϙ�+6�w.Laa2�~�?s�����"�<�i&��Ps��~�KԾu%۞��Lč_��v���D�[��
��+��Y������״���"\y75n0A�ӊ/��lSx�>ư���Z9\�6��C3��j8�V���g����������t�|Y��9�w"��D/�"ۃ���<s.���t�m����Y����b��经G��;kY�eh����b�%V�}ӟa=�.��(����oG�;i	f���,�27�~�z�꿅�!k      .   "   x���	q��wt�s�LK�)N����� j      -   �  x�eR�n�0<���E�B >��5��p��zK�ba�6�Hr)	n},�k��k4�K	�3�Cfp۴�����9}?�0�z�����/����D���1��;��H����AJ.���L�J�NE�
��[ ��k������:�����z��x3p�{�������'�U�P%1)�V���n���->�֒�n5�(RQ�z�#I����N�Z�GEڄ�PG;g�/}�!���� �+׏^��4���c�\^�؊���H�*�BI�H���&'�:�(��!(�)Y�*Z�@flЅVx����s�q�g�?�iw�\�f�h���uu�l*�B�2�jh줦Q�����l.���l��;|��=�����A� ����i�h�������g����y�f��s����)�ΙwBbWw=��-�#�}ڶ�^n�}�s^����<�	������|�$�_�O�g     