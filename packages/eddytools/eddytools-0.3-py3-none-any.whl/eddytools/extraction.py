import os
import time
from pkg_resources import resource_stream

# SQLAlchemy imports
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, ResultProxy, Transaction, Connection
from sqlalchemy.schema import MetaData, Table
from sqlalchemy.schema import UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.sql import func, select, text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import types
from sqlalchemy import inspect
from tqdm import tqdm
from datetime import datetime
from sqlitedict import SqliteDict


# OpenSLEX parameters
_OPENSLEX_SCRIPT_PATH = 'resources/metamodel.sql'


# create a SQLite database file for the OpenSLEX mm and run the script to create all tables
def create_mm(mm_file_path, overwrite=False):
    is_success = False

    # check if file already exists
    if os.path.exists(mm_file_path):
        if overwrite:
            try:
                print("Removing OpenSLEX MM")
                os.remove(mm_file_path)
            except Exception as e:
                raise
        else:
            raise Exception("File already exists")

    # if directory doesn't exist, create directory
    openslex_dir = os.path.dirname(mm_file_path)
    if not os.path.exists(openslex_dir):
        os.makedirs(openslex_dir)

    is_connected = False

    try:
        print("Opening OpenSLEX MM")
        mm_engine = create_mm_engine(mm_file_path)
        conn = mm_engine.raw_connection()
        is_connected = True
        cursor = conn.cursor()

        print("Reading script")
        stream = resource_stream(__name__, _OPENSLEX_SCRIPT_PATH)
        script = stream.read().decode()

        print("Running script")
        cursor.executescript(script)
        conn.commit()
        conn.close()
        mm_engine.dispose()
        is_connected = False
        print("OpenSLEX MM succesfully created")

    except Exception as e:
        if is_connected:
            print("Closing DB")
            conn.close()
            mm_engine.dispose()
            is_connected = False
        raise e


# create engine for the OpenSLEX mm using SQLAlchemy
def create_mm_engine(openslex_file_path):
    mm_url = 'sqlite:///{path}'.format(path=openslex_file_path)
    engine = create_engine(mm_url)
    return engine


# create engine for the source database using SQLAlchemy
def create_db_engine(dialect=None, host=None, username=None, password=None, port=None,
                           database=None, trusted_conn=False, **params):
    db_url = '{}://'.format(dialect)
    if not trusted_conn:
        if username:
            db_url += '{username}'.format(username=username)
            if password:
                db_url += ':{password}'.format(password=password)
            db_url += '@'
    if host:
        db_url += host
    if port:
        db_url += ':{}'.format(port)
    if database:
        db_url += '/{}'.format(database)
    engine = create_engine(db_url, pool_pre_ping=True, connect_args=params)
    return engine


def create_db_engine_from_url(db_url, **params):
    engine = create_engine(db_url, pool_pre_ping=True, connect_args=params)
    return engine


def get_metadata(db_engine: Engine, schemas=None) -> MetaData:
    metadata = MetaData(bind=db_engine)
    metadata.tables = dict()
    if not schemas:
        insp = inspect(db_engine)
        schemas = insp.get_schema_names()
    for schema in schemas:
        m = MetaData(bind=db_engine)
        m.reflect(schema=schema)
        for t in m.tables.values():
            metadata.tables[t.fullname] = t
    return metadata


# reflect the metadata of the OpenSLEX mm into a SQLAlchemy MetaData object
def get_mm_meta(mm_engine):
    mm_meta = MetaData()
    mm_meta.reflect(bind=mm_engine)
    return mm_meta


# insert values into table t using conn
def insert_values(conn, t, values):
    trans = conn.begin()
    try:
        q = t.insert().values(values)
        res = conn.execute(q)
        trans.commit()
    except:
        trans.rollback()
        raise

    return res


# get the data type of a column (integer, string, boolean, numeric, timestamp)
def get_data_type(col):
    if isinstance(col.type, types.Integer):
        return 'integer'
    elif isinstance(col.type, types.String):
        return 'string'
    elif isinstance(col.type, types.Boolean):
        return 'boolean'
    elif isinstance(col.type, types.Numeric):
        return 'numeric'
    elif isinstance(col.type, (types.Date, types.DateTime, types.Time)):
        return 'timestamp'


'''
insert the metadata of the source database (classes, attributes and relationships) into the OpenSLEX mm
returns:
class_map: mapping class_name --> class_id in the OpenSLEX mm
attr_map: mapping (class_name, attribute_name) --> attribute_id in the OpenSLEX mm
rel_map: mapping (class_name, relationship_name) --> relationship_id in the OpenSLEX mm
'''


def insert_metadata(mm_conn, mm_meta: MetaData, db_meta: MetaData, dm_name, classes = None):
    class_map = dict()
    attr_map = dict()
    rel_map = dict()

    trans = mm_conn.begin()
    try:

        dm_table = mm_meta.tables.get('datamodel')
        dm_values = {'name': dm_name}
        res_ins_dm = insert_values(mm_conn, dm_table, dm_values)
        dm_id = res_ins_dm.inserted_primary_key[0]
        if not classes:
            db_classes = [t.fullname for t in db_meta.tables.values()]
        else:
            db_classes = classes
        for c in tqdm(db_classes, desc='Inserting Class Metadata'):
            class_table = mm_meta.tables.get('class')
            class_values = {'datamodel_id': dm_id, 'name': c}
            res_ins_class = insert_values(mm_conn, class_table, class_values)
            class_id = res_ins_class.inserted_primary_key[0]
            class_map[c] = class_id

            attrs = db_meta.tables.get(c).c
            for attr in attrs:
                if get_data_type(attr):
                    attr_table = mm_meta.tables.get('attribute_name')
                    attr_values = {'class_id': class_id, 'name': attr.name, 'type': get_data_type(attr)}
                    res_ins_col = insert_values(mm_conn, attr_table, attr_values)
                    attr_id = res_ins_col.inserted_primary_key[0]
                    attr_map[(c, attr.name)] = attr_id

        for c in tqdm(db_classes, desc='Inserting Class Relationships'):
            fkcs = db_meta.tables.get(c).foreign_key_constraints
            for fkc in fkcs:
                if fkc.referred_table.fullname in class_map:
                    rel_table = mm_meta.tables.get('relationship')
                    rel_values = {'source': class_map[c],
                                  'target': class_map[fkc.referred_table.fullname],
                                  'name': fkc.name}
                    res_ins_rel = insert_values(mm_conn, rel_table, rel_values)
                    rel_id = res_ins_rel.inserted_primary_key[0]
                    rel_map[(c, fkc.name)] = rel_id

        trans.commit()
    except:
        trans.rollback()
        raise

    return class_map, attr_map, rel_map


# insert object, object version, object attribute values into the OpenSLEX mm for one object in the source db
def insert_object(mm_conn, obj, source_table, class_name, class_map, attr_map,
                  rel_map, obj_v_map, obj_hash_map, mm_meta):
    trans = mm_conn.begin()
    try:
        # insert into object table
        obj_table = mm_meta.tables.get('object')
        obj_values = {'class_id': class_map[class_name]}
        res_ins_obj = insert_values(mm_conn, obj_table, obj_values)
        obj_id = res_ins_obj.inserted_primary_key[0]

        # insert into object_version table
        obj_v_table = mm_meta.tables.get('object_version')
        obj_v_values = {'object_id': obj_id, 'start_timestamp': -2, 'end_timestamp': -1}
        res_ins_obj_v = insert_values(mm_conn, obj_v_table, obj_v_values)
        obj_v_id = res_ins_obj_v.inserted_primary_key[0]
        # pk_tuple = tuple(col.name for col in source_table.primary_key.columns)
        # pk_values_tuple = tuple(obj[col] for col in pk_tuple)
        # obj_v_map[(class_name, pk_tuple, pk_values_tuple)] = obj_v_id

        unique_constraints = [uc for uc in source_table.constraints if isinstance(uc, (UniqueConstraint,
                                                                                       PrimaryKeyConstraint))]
        notunique = True
        for uc in unique_constraints:
            if uc.columns:
                notunique = False
                unique_tuple = tuple(col.name for col in uc)
                unique_values_tuple = tuple(obj[col] for col in unique_tuple)
                v_tuple = (class_name, unique_tuple, unique_values_tuple)
                _set_v_id_for_values(obj_v_map, obj_hash_map, v_tuple, obj_v_id)

        if notunique:
            unique_tuple = tuple(col.name for col in source_table.columns)
            unique_values_tuple = tuple(obj[col] for col in unique_tuple)
            v_tuple = (class_name, unique_tuple, unique_values_tuple)
            _set_v_id_for_values(obj_v_map, obj_hash_map, v_tuple, obj_v_id)

        # insert into attribute_value table
        attr_v_table = mm_meta.tables.get('attribute_value')

        attr_v_values = []
        for attr in obj.items():
            if ((class_name, attr[0]) in attr_map.keys()) and attr[1]:
                 attr_v_values.append(
                     {'object_version_id': obj_v_id,
                      'attribute_name_id': attr_map[(class_name, attr[0])],
                      'value': str(attr[1])
                      })

        res_ins_attr_v = insert_values(mm_conn, attr_v_table, attr_v_values)
        trans.commit()
    except:
        trans.rollback()
        raise


def _get_dict_from_cursor(cursor):
    tup = cursor.fetchone()

    obj = None

    if tup:
        obj = dict()
        for i, c in enumerate(cursor.description):
            obj[c[0]] = tup[i]

    return obj


# insert all objects of one class into the OpenSLEX mm
def insert_class_objects(mm_conn: Connection, mm_meta, db_engine, db_meta, class_name,
                         class_map, attr_map, rel_map, obj_v_map, obj_hash_map):
    t1 = time.time()
    trans: Transaction = mm_conn.begin()
    try:
        source_table: Table = db_meta.tables.get(class_name)
        num_objs = db_engine.execute(source_table.count()).scalar()

        q = source_table.select()
        conn = db_engine.raw_connection()
        cursor = conn.cursor()
        cursor.execute(str(q.compile(dialect=db_engine.dialect, compile_kwargs={"literal_binds": True})))

        i = 0
        obj = _get_dict_from_cursor(cursor)
        with tqdm(desc='Objects', total=num_objs) as tpb:
            while obj:
                insert_object(mm_conn, obj, source_table, class_name, class_map,
                              attr_map, rel_map, obj_v_map, obj_hash_map, mm_meta)
                obj = _get_dict_from_cursor(cursor)
                tpb.update(1)
                i += 1
                if i > 1000:
                    i = 0
                    try:
                        obj_v_map.sync()
                        obj_hash_map.sync()
                    except:
                        pass

        trans.commit()
    except:
        trans.rollback()
        raise
    t2 = time.time()
    time_diff = t2 - t1


def _set_v_id_for_values(v_map, hash_map, values, id):
    v_str = str(values)
    v_hash = v_str.__hash__()

    idlist = v_map.get(v_hash, [])
    idlist.append(id)
    v_map[v_hash] = idlist

    vlist = hash_map.get(v_hash, [])
    vlist.append(values)
    hash_map[v_hash] = vlist


def _get_v_id_for_values(v_map, hash_map, values):
    id = None

    v_str = str(values)
    v_hash = v_str.__hash__()

    vlist = hash_map.get(v_hash, [])

    for i, v in enumerate(vlist):
        if v == values:
            idlist = v_map.get(v_hash)
            id = idlist[i]
            break

    return id


# insert the relations of one object into the OpenSLEX mm
def insert_object_relations(mm_conn, mm_meta, obj, source_table: Table, class_name,
                            rel_map, obj_v_map, obj_hash_map):
    trans = mm_conn.begin()
    try:
        rel_table = mm_meta.tables.get('relation')
        for fkc in source_table.foreign_key_constraints:
            tuple_foreign_cols = tuple(fk.column.name for fk in fkc.elements)
            tuple_cols = tuple(col.name for col in fkc.columns)
            target_obj_v_params = (
                fkc.referred_table.fullname,
                tuple_foreign_cols,
                tuple(obj[col] for col in tuple_cols)
            )
            target_obj_v_id = _get_v_id_for_values(obj_v_map, obj_hash_map, target_obj_v_params)
            if target_obj_v_id:
                if not source_table.primary_key or not source_table.primary_key.columns:
                    tuple_cols = tuple(col.name for col in source_table.columns)
                    source_obj_v_id = _get_v_id_for_values(
                        obj_v_map, obj_hash_map, (source_table.fullname,
                                                  tuple_cols,
                                                  tuple(obj[col] for col in tuple_cols)))
                    # source_obj_v_id = obj_v_map[str((
                    #     source_table.fullname,
                    #     tuple_cols,
                    #     tuple(obj[col] for col in tuple_cols)
                    # ))]
                else:
                    tuple_cols = tuple(col.name for col in source_table.primary_key.columns)
                    source_obj_v_id = _get_v_id_for_values(
                        obj_v_map, obj_hash_map, (source_table.fullname,
                                                  tuple_cols,
                                                  tuple(obj[col] for col in tuple_cols)))
                    # source_obj_v_id = obj_v_map[str((
                    #     source_table.fullname,
                    #     tuple_cols,
                    #     tuple(obj[col] for col in tuple_cols)
                    # ))]
                rel_value = [{
                    'source_object_version_id': source_obj_v_id,
                    'target_object_version_id': target_obj_v_id,
                    'relationship_id': rel_map[(class_name, fkc.name)],
                    'start_timestamp': -2,
                    'end_timestamp': -1
                }]
                res_ins_rel = insert_values(mm_conn, rel_table, rel_value)

        trans.commit()
    except Exception:
        trans.rollback()
        raise


# insert the relations of all objects of one class into the OpenSLEX mm
def insert_class_relations(mm_conn, mm_meta, db_engine, db_meta, class_name,
                           rel_map, obj_v_map, obj_hash_map):
    t1 = time.time()
    trans = mm_conn.begin()
    try:
        source_table: Table = db_meta.tables.get(class_name)
        num_objs = db_engine.execute(source_table.count()).scalar()

        q = source_table.select()
        conn = db_engine.raw_connection()
        cursor = conn.cursor()
        cursor.execute(str(q.compile(dialect=db_engine.dialect, compile_kwargs={"literal_binds": True})))

        i = 0
        obj = _get_dict_from_cursor(cursor)
        with tqdm(desc='Relations', total=num_objs) as tpb:
            while obj:
                insert_object_relations(mm_conn, mm_meta, obj, source_table, class_name,
                                        rel_map, obj_v_map, obj_hash_map)
                obj = _get_dict_from_cursor(cursor)
                tpb.update(1)
                i += 1
                if i > 1000:
                    i = 0
                    try:
                        obj_v_map.sync()
                        obj_hash_map.sync()
                    except:
                        pass

        trans.commit()

        # source_table = db_meta.tables.get(class_name)
        # num_objs = db_engine.execute(source_table.count()).scalar()
        # objs = db_engine.execute(source_table.select())
        # for obj in tqdm(objs, total=num_objs, desc='Relations'):
        #     insert_object_relations(mm_conn, mm_meta, obj, source_table, class_name, rel_map, obj_v_map)
        # trans.commit()
    except:
        trans.rollback()
        raise
    t2 = time.time()
    time_diff = t2 - t1


# insert the objects of all classes of the source db into the OpenSLEX mm
def insert_objects(mm_conn, mm_meta, db_engine, db_meta, classes, class_map, attr_map, rel_map, cache_dir):
    obj_v_map = SqliteDict(
        flag='n',
        filename='{}/{}-{}'.format(cache_dir, 'obj_v_map_filecache', datetime.now().timestamp()),
        autocommit=True)

    obj_hash_map = SqliteDict(
        flag='n',
        filename='{}/{}-{}'.format(cache_dir, 'obj_hash_map_filecache', datetime.now().timestamp()),
        autocommit=True)

    with tqdm(classes, desc='Inserting Class Objects') as tpb:
        for class_name in tpb:
            tpb.set_postfix_str(class_name, refresh=True)
            insert_class_objects(mm_conn, mm_meta, db_engine, db_meta, class_name,
                                 class_map, attr_map, rel_map, obj_v_map, obj_hash_map)
            obj_v_map.sync()
            obj_hash_map.sync()

    with tqdm(classes, desc='Inserting Class Relations') as tpb:
        for class_name in tpb:
            tpb.set_postfix_str(class_name, refresh=True)
            insert_class_relations(mm_conn, mm_meta, db_engine, db_meta, class_name,
                                   rel_map, obj_v_map, obj_hash_map)
            obj_v_map.sync()
            obj_hash_map.sync()

    try:
        obj_v_map.close()
        obj_hash_map.close()
    except:
        pass


def extract_to_mm(openslex_file_path, connection_params, cache_dir, db_engine=None, schemas=None,
                  overwrite=False, classes=None, metadata=None):
    # connect to the OpenSLEX mm
    try:
        create_mm(openslex_file_path, overwrite)
        mm_engine = create_mm_engine(openslex_file_path)
        if not db_engine:
            db_engine = create_db_engine(**connection_params)
        if metadata:
            db_meta = metadata
        else:
            db_meta = get_metadata(db_engine, schemas)
        mm_meta = get_mm_meta(mm_engine)
        dm_name = connection_params.get('database', 'DataModel')
    except Exception as e:
        raise e

    extraction_from_db(openslex_file_path, cache_dir, db_engine, overwrite,
                       classes, metadata)


def extraction_from_db(openslex_file_path, cache_dir, db_engine=None,
                       overwrite=False, classes=None, metadata=None):
    # connect to the OpenSLEX mm
    try:
        create_mm(openslex_file_path, overwrite)
        mm_engine = create_mm_engine(openslex_file_path)
        db_meta = metadata
        mm_meta = get_mm_meta(mm_engine)
        dm_name = 'datamodel'
    except Exception as e:
        raise e

    # insert the source's datamodel into the OpenSLEX mm
    t1 = time.time()
    mm_conn = mm_engine.connect()
    try:
        class_map, attr_map, rel_map = insert_metadata(mm_conn, mm_meta, db_meta, dm_name, classes)
    except Exception as e:
        raise e
    mm_conn.close()
    t2 = time.time()
    time_diff = t2 - t1

    # insert objects into the OpenSLEX mm
    t1 = time.time()
    mm_conn = mm_engine.connect()
    try:
        if classes is None:
            classes = [t.fullname for t in db_meta.tables.values()]
        insert_objects(mm_conn, mm_meta, db_engine,
                       db_meta, classes, class_map,
                       attr_map, rel_map, cache_dir)
    except Exception as e:
        raise e
    mm_conn.close()
    mm_engine.dispose()
    db_engine.dispose()
    t2 = time.time()
    time_diff = t2 - t1
